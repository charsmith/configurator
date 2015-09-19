import unittest
from configurator import Configurator as C

from nose.tools import assert_equals, raises

class TestSetup(unittest.TestCase):
    def test_config(self):
        C.initialize(["--config", "field.name=blah"])
        assert_equals("blah", C.get("field", "name"))

    @raises(SystemExit)
    def test_bad_property(self):
        C.initialize(["--config", "fieldname=blah"])

    @raises(SystemExit)
    def test_no_value(self):
        C.initialize(["--config", "field.name"])

    def test_argv(self):
        C.initialize(["--config", "field.name=blah", "--foo", "blah"])
        assert_equals(["--foo", "blah"], C.argv)

    def test_multiple_config(self):
        C.initialize(["--config", "field.name=blah",
            "--config", "other.prop=foo",
            "--config", "bool.prop=True"])
        assert_equals("foo", C.get("other", "prop"))
        assert_equals("blah", C.get("field", "name"))
        assert_equals(True, C.getboolean("bool", "prop"))

    def test_env(self):
        import os
        os.environ["test_prop"] = "something"
        os.environ["bool_prop"] = "False"
        assert_equals("something", C.get("test", "prop"))
        assert_equals(False, C.getboolean("bool", "prop"))

    def test_env_override(self):
        import os
        os.environ["test_prop"] = "something"
        os.environ["bool_prop"] = "False"
        C.initialize(["--config", "test.prop=blah",
            "--config", "bool.prop=True"])
        assert_equals("blah", C.get("test", "prop"))
        assert_equals(True, C.getboolean("bool", "prop"))

    def test_boolean_states(self):
        C.initialize([
             "--config", "bool.true1=True"
            ,"--config", "bool.true2=true"
            ,"--config", "bool.true3=TRUE"
            ,"--config", "bool.true4=1"
            ,"--config", "bool.true5=on"
            ,"--config", "bool.true6=ON"
            ,"--config", "bool.false1=False"
            ,"--config", "bool.false2=false"
            ,"--config", "bool.false3=FALSE"
            ,"--config", "bool.false4=0"
            ,"--config", "bool.false5=off"
            ,"--config", "bool.false6=OFF"
        ])
        assert_equals(True, C.getboolean("bool","true1"))
        assert_equals(True, C.getboolean("bool","true2"))
        assert_equals(True, C.getboolean("bool","true3"))
        assert_equals(True, C.getboolean("bool","true4"))
        assert_equals(True, C.getboolean("bool","true5"))
        assert_equals(True, C.getboolean("bool","true6"))
        assert_equals(False, C.getboolean("bool","false1"))
        assert_equals(False, C.getboolean("bool","false2"))
        assert_equals(False, C.getboolean("bool","false3"))
        assert_equals(False, C.getboolean("bool","false4"))
        assert_equals(False, C.getboolean("bool","false5"))
        assert_equals(False, C.getboolean("bool","false6"))

    def test_valid_formats(self):
        C.initialize([
            "--config", "value.one=One",
            "--config", "value.two=Two"
        ])
        assert_equals("One", C.get('value', 'one', 'Three'), C.get('value.one', 'Two'))
        assert_equals('Two', C.get('value.two'), C.get('value', 'two'))
        assert_equals('Three', C.get('value.three', 'Three'), C.get('value', 'three', 'Three'))
        assert_equals(None, C.get('value.four'), C.get('value', 'four'))

    def test_int(self):
        C.initialize([
            "--config", "value.one=1"
        ])
        assert_equals('1', C.get('value', 'one', '3'))
        assert_equals('1', C.get('value.one', '2'))
        assert_equals(1, C.getint('value.one'))
        assert_equals(1, C.getint('value', 'one'))
        assert_equals(3, C.getint('value.three', '3'))
        assert_equals(3, C.getint('value', 'three', '3'))
        assert_equals(3, C.getint('value.three', 3))
        assert_equals(None, C.getint('value.four'))
        assert_equals(None, C.getint('value', 'four'))

    def test_case(self):
        C.initialize([
            "--config", "env.VARIABLE=1"
        ])
        assert_equals([('VARIABLE', '1')], C.config.items('env'))
