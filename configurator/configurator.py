import argparse
import ConfigParser
import os
import sys

def addOption(option, config):
    assert option is not None, "--config must be followed by an argument"
    try:
        (k, v) = option.split('=',1)
        section, key = k.split('.')
    except:
        print "Arguments to config option are malformed: %s" % (option)
        print "Use the following form: --config section.key=value"
        exit(1)
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, v)

def addOptionFile(filename, config):
    config.read(filename)

class Configurator(object):
    @classmethod
    def initialize(cls, args=None):
        cls.config = ConfigParser.SafeConfigParser({})

        parser = argparse.ArgumentParser()
        parser.add_argument("--config",
                        action="append",
                        default=[],
                        help="Add a new option to the configuration.  Options "
                            "should be in the format: section.key=value")
        parser.add_argument("--configFile",
                        action="append",
                        default=[],
                        help="Add a new optionFile to the configuration. The file"
                            "should be in ini file format, readable by "
                            "ConfigParser")

        (namespace, argv) = parser.parse_known_args(args)
        cls.argv = argv

        if os.path.exists('ini'):
            for filename in [fn for fn in os.listdir('ini')
                    if not fn.startswith('.')
                        and not fn.startswith('~')
                        and not fn.endswith('~')
                        and not fn.endswith('.swp')]:
                addOptionFile('ini/' + filename, cls.config)

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
        env = os.environ.get('%s_%s' % (section, option))
        if not env:
            return default
        return env

    @classmethod
    def get(cls, section, *args, **kwargs):
        if '.' in section:
            section, option = section.split('.', 1)
            return cls._get(section, option, *args, **kwargs)
        return cls._get(section, *args, **kwargs)

    @classmethod
    def _get(cls, section, option, default=None, raw=True, blank_default=False):
        try:
            ret = cls.config.get(section, option, raw=raw)
            if blank_default and not ret:
                return cls.__get_env(section, option, default=default)
            return ret
        except ConfigParser.NoOptionError:
            return cls.__get_env(section, option, default=default)
        except ConfigParser.NoSectionError:
            return cls.__get_env(section, option, default=default)

    @classmethod
    def getboolean(cls, *args, **kwargs):
        ret = cls.get(*args, **kwargs)
        if str(ret).lower() not in cls.config._boolean_states:
            raise ValueError, 'Not a boolean: %s' % str(ret)
        return cls.config._boolean_states[str(ret).lower()]

Configurator.initialize(sys.argv)
