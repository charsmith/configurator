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
