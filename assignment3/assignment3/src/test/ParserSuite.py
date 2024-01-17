import unittest
from TestUtils import TestParser


class ParserSuite(unittest.TestCase):
    def test_for_checker(self):
        input = """
        parent : function void() {}
        child : function void() inherit parent {
            super();
        }
        main:function void() {
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 400))
