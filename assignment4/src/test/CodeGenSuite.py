import unittest
from TestUtils import TestCodeGen
from AST import *
## Truong Hong Hoa
## 1911185

class CheckCodeGenSuite(unittest.TestCase):
    def test_global_declaration(self):
        input = """
        foo : function integer(a: integer){
            
        }
        main: function void(){
        }
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input,expect,500))
    
    # def test_global_declaration2(self):
    #     input = """
    #     a : integer = 1;
    #     main: function void(){
    #     }
    #     """
    #     expect = ""
    #     self.assertTrue(TestCodeGen.test(input,expect,501))
    
    # def test_callstmt_builtin_1(self):
    #     input = """
    #     main: function void(){
    #         printInteger(1);
    #     }
    #     """
    #     expect = "1"
    #     self.assertTrue(TestCodeGen.test(input,expect,502))
    
