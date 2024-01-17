import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_function_main(self):
        input = """
        main: function void () {
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input, expect, 400))
        
        
        