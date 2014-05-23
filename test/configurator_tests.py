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
            "--config", "other.prop=foo"])
        assert_equals("foo", C.get("other", "prop"))
        assert_equals("blah", C.get("field", "name"))

    def test_env(self):
        import os
        os.environ["test_prop"] = "something"
        assert_equals("something", C.get("test", "prop"))

    def test_env_override(self):
        import os
        os.environ["test_prop"] = "something"
        C.initialize(["--config", "test.prop=blah"])
        assert_equals("blah", C.get("test", "prop"))
