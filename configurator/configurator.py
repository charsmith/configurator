from __future__ import print_function, unicode_literals
from future import standard_library

standard_library.install_aliases()
from builtins import str
from builtins import object
import builtins
import argparse
import functools
import os
import sys
from future.utils import with_metaclass

if sys.version_info >= (3, 0):
    import configparser
else:
    import ConfigParser as configparser


def addOption(option, config):
    assert option is not None, "--config must be followed by an argument"
    try:
        (k, v) = option.split("=", 1)
        section, key = k.split(".")
        if not config.has_section(section):
            config.add_section(section)
        configparser.ConfigParser.set(config, section, key, v)
    except:
        if os.environ.get("CONFIGURATOR", "").lower() == "loud":
            print("Arguments to config option are malformed: %s" % (option))
            print("Use the following form: --config section.key=value")
            exit(1)


def addOptionFile(filename, config):
    config.read(filename)


class ConfiguratorType(type):
    def __wrapper(cls, type_name, *args, **kwargs):
        v = cls.get(*args, **kwargs)
        return None if v is None else getattr(builtins, type_name)(v)

    def __getattr__(cls, key):
        if key.startswith("get"):
            type_name = key[3:]
            return functools.partial(cls.__wrapper, type_name)
        raise AttributeError(key)


# monkeypatch argparse so that --conf doesn't affect config and configFile
# this works in 2.7 and 3.5 although in 3.5 there is an option to change the behavior
def _get_option_tuples(option_string):
    result = []
    return result


class Configurator(with_metaclass(ConfiguratorType, object)):
    @classmethod
    def initialize(cls, args=None):
        cls.config = configparser.SafeConfigParser({})
        cls.config.optionxform = str

        parser = argparse.ArgumentParser(add_help=False)
        parser._get_option_tuples = _get_option_tuples
        parser.add_argument(
            "--config",
            action="append",
            default=[],
            help="Add a new option to the configuration.  Options "
            "should be in the format: section.key=value",
        )
        parser.add_argument(
            "--configFile",
            action="append",
            default=[],
            help="Add a new optionFile to the configuration. The file"
            "should be in ini file format, readable by "
            "ConfigParser",
        )

        (namespace, argv) = parser.parse_known_args(args)
        cls.argv = argv

        if os.path.exists("ini"):
            for filename in [
                fn
                for fn in os.listdir("ini")
                if not fn.startswith(".")
                and not fn.startswith("~")
                and not fn.endswith("~")
                and not fn.endswith(".swp")
            ]:
                addOptionFile("ini/" + filename, cls.config)

        for filename in namespace.configFile:
            addOptionFile(filename, cls.config)

        for option in namespace.config:
            addOption(option, cls.config)

    @classmethod
    def addOptionFile(cls, filename):
        addOptionFile(filename, cls.config)
        return cls

    @classmethod
    def addOption(cls, option):
        addOption(option, cls.config)
        return cls

    @classmethod
    def set(cls, section, option, value):
        if not cls.config.has_section(section):
            cls.config.add_section(section)
        cls.config.set(section, option, value)

    @classmethod
    def __get_env(cls, section, option, default=None):
        env = os.environ.get("%s_%s" % (section, option))
        if not env:
            return default
        return env

    @classmethod
    def get(cls, section, *args, **kwargs):
        if "." in section:
            section, option = section.split(".", 1)
            return cls._get(section, option, *args, **kwargs)
        return cls._get(section, *args, **kwargs)

    @classmethod
    def _get(cls, section, option, default=None, raw=True, blank_default=False):
        try:
            ret = cls.config.get(section, option, raw=raw)
            if blank_default and not ret:
                return cls.__get_env(section, option, default=default)
            return ret
        except configparser.NoOptionError:
            return cls.__get_env(section, option, default=default)
        except configparser.NoSectionError:
            return cls.__get_env(section, option, default=default)

    @classmethod
    def getboolean(cls, *args, **kwargs):
        if sys.version_info >= (3, 0):
            boolean_states = cls.config.BOOLEAN_STATES
        else:
            boolean_states = cls.config._boolean_states
        ret = cls.get(*args, **kwargs)
        if str(ret).lower() not in boolean_states:
            raise ValueError("Not a boolean: %s" % str(ret))
        return boolean_states[str(ret).lower()]


Configurator.initialize(sys.argv)
