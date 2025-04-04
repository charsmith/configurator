import unittest
import pytest
from configurator import Configurator as C


class TestSetup(unittest.TestCase):
    def test_config(self):
        C.initialize(["--config", "field.name=blah"])
        assert "blah" == C.get("field", "name")

    def test_bad_property(self):
        import os

        os.environ["CONFIGURATOR"] = "loud"
        with pytest.raises(SystemExit):
            C.initialize(["--config", "fieldname=blah"])

    def test_quiet_bad_property(self):
        import os

        del os.environ["CONFIGURATOR"]
        C.initialize(["--config", "fieldname=blah"])

    def test_no_value(self):
        with pytest.raises(SystemExit):
            C.initialize(["--config", "field.name"])

    def test_argv(self):
        C.initialize(["--config", "field.name=blah", "--foo", "blah"])
        assert ["--foo", "blah"] == C.argv

    def test_multiple_config(self):
        C.initialize(
            [
                "--config",
                "field.name=blah",
                "--config",
                "other.prop=foo",
                "--config",
                "bool.prop=True",
            ]
        )
        assert "foo" == C.get("other", "prop")
        assert "blah" == C.get("field", "name")
        assert C.getboolean("bool", "prop")

    def test_env(self):
        import os

        os.environ["test_prop"] = "something"
        os.environ["bool_prop"] = "False"
        assert "something", C.get("test", "prop")
        assert not C.getboolean("bool", "prop")

    def test_env_override(self):
        import os

        os.environ["test_prop"] = "something"
        os.environ["bool_prop"] = "False"
        C.initialize(["--config", "test.prop=blah", "--config", "bool.prop=True"])
        assert "blah" == C.get("test", "prop")
        assert C.getboolean("bool", "prop")

    def test_boolean_states(self):
        C.initialize(
            [
                "--config",
                "bool.true1=True",
                "--config",
                "bool.true2=true",
                "--config",
                "bool.true3=TRUE",
                "--config",
                "bool.true4=1",
                "--config",
                "bool.true5=on",
                "--config",
                "bool.true6=ON",
                "--config",
                "bool.false1=False",
                "--config",
                "bool.false2=false",
                "--config",
                "bool.false3=FALSE",
                "--config",
                "bool.false4=0",
                "--config",
                "bool.false5=off",
                "--config",
                "bool.false6=OFF",
            ]
        )
        assert C.getboolean("bool", "true1")
        assert C.getboolean("bool", "true2")
        assert C.getboolean("bool", "true3")
        assert C.getboolean("bool", "true4")
        assert C.getboolean("bool", "true5")
        assert C.getboolean("bool", "true6")
        assert not C.getboolean("bool", "false1")
        assert not C.getboolean("bool", "false2")
        assert not C.getboolean("bool", "false3")
        assert not C.getboolean("bool", "false4")
        assert not C.getboolean("bool", "false5")
        assert not C.getboolean("bool", "false6")

    def test_valid_formats(self):
        C.initialize(["--config", "value.one=One", "--config", "value.two=Two"])
        assert C.get("value", "one", "Three") == "One"
        assert C.get("value.one", "Two") == "One"
        assert C.get("value.two") == "Two"
        assert C.get("value", "two") == "Two"
        assert C.get("value.three", "Three") == "Three"
        assert C.get("value", "three", "Three") == "Three"
        assert C.get("value.four") is None
        assert C.get("value", "four") is None

    def test_int(self):
        C.initialize(["--config", "value.one=1"])
        assert C.get("value", "one", "3") == "1"
        assert C.get("value.one", "2") == "1"
        assert C.getint("value.one") == 1
        assert C.getint("value", "one") == 1
        assert C.getint("value.three", "3") == 3
        assert C.getint("value", "three", "3") == 3
        assert C.getint("value.three", 3) == 3
        assert C.getint("value.four") is None
        assert C.getint("value", "four") is None

    def test_case(self):
        C.initialize(["--config", "env.VARIABLE=1"])
        assert C.config.items("env") == [("VARIABLE", "1")]

    def test_conf(self):
        C.initialize(["--conf", "env.VARIABLE=1", "--config", "blah.blah=2"])
        assert C.get("blah.blah") == "2"
