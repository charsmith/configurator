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
