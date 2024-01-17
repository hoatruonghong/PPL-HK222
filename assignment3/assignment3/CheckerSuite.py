import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    
    def test_decl_order(self):
        input = """
        a : integer = 1;
        main: function void() {
            res : auto = readString();
            b: integer = a;
            res = foo() + foo(2); 
        }
        foo : function auto (){}
        """
        expect = "Type mismatch in expression: FuncCall(foo, [IntegerLit(2)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_decl_order_2(self):
        input = """
        main: function void() {
            res : auto = readString();
            b: integer = a;
        }
        foo : function auto (){}
        a : integer = 1;
        """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    
    def test_name_simple_1(self):
        input = """
        main: function void(){
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_2(self):
        input = """
        a,b,c,a: integer;
        main: function void(){
        }
        """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_3(self):
        input = """
        a: integer;
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_5(self):
        input = """
        main: function integer(){}
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,400))
        
    def test_name_simple_6(self):
        input = """
        main: function void(a: integer){}
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_7(self):
        input = """
        foo: function integer (){}
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_8(self):
        input = """
        foo: function integer (){}
        main: function void(){}
        height, weight : integer;
        foo : integer;
        """
        expect = "Redeclared Variable: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_9(self):
        input = """
        main: function void() {
        }
        main: function void() {
        }
        """
        expect = "Redeclared Function: main"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_name_simple_10(self):
        input = """
        main: function void(){}
        height, weight : integer;
        readInteger : integer;
        """
        expect = "Redeclared Variable: readInteger"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_vardecl_1(self):
        input = """
        main: function void() {}
        a: auto;
        """
        expect = "Invalid Variable: a"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_vardecl_2(self):
        input = """
        main: function void(){}
        a, b, c, d: auto = 1, 2.5, "My name is Hoa", true;
        e : integer = 2.5;
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(e, IntegerType, FloatLit(2.5))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_vardecl_3(self):
        input = """
        area : float = 2.5;
        an : float = 1 ;
        x : float = true;
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(x, FloatType, BooleanLit(True))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_1(self):
        input = """
        arr : array [3] of integer = {1,2,3.3};
        main: function void(){}
        """
        expect = "Illegal array literal: ArrayLit([IntegerLit(1), IntegerLit(2), FloatLit(3.3)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_2(self):
        input = """
        arr : array [3] of integer = {1.0,2.2,3.3};
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(arr, ArrayType([3], IntegerType), ArrayLit([FloatLit(1.0), FloatLit(2.2), FloatLit(3.3)]))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_3(self):
        input = """
        arr : array [2,3,4,5] of integer;
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_7(self):
        input = """
        arr : array [2] of integer = {1,2};
        a : float = 1.0;
        element : integer = arr[a];
        main: function void(){
            
        }
        """
        expect = "Type mismatch in expression: ArrayCell(arr, [Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_8(self):
        input = """
        a : float = 1.0;
        element : integer = a[1.0];
        main: function void(){
        }
        """
        expect = "Type mismatch in expression: ArrayCell(a, [FloatLit(1.0)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_9(self):
        input = """
        element : string = arr[10];
        main: function void(){
        }
        """
        expect = "Undeclared Identifier: arr"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_array_10(self):
        input = """
        arr : array [5] of integer = {0,1,2,3,4};
        element : integer = arr[arr[0]];
        main: function void(){
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))

    # test expr : check - declared -> type
    def test_expr_type_1(self):
        input = """
        a : integer = 3;
        b: integer = a + "halo";
        main: function void(){}
        """
        expect = "Type mismatch in expression: BinExpr(+, Id(a), StringLit(halo))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_block_1(self):
        input = """
        a : integer = 1;
        main: function void(){
            a,b : float;
            b : integer = 3;
        }
        """
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_function_auto_1(self):
        input = """
        foo : function auto ( a : integer , b : integer ) {}
        a : float = foo(1,2);
        b : integer = foo(1,2);
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(b, IntegerType, FuncCall(foo, [IntegerLit(1), IntegerLit(2)]))"
        self.assertTrue(TestChecker.test(input,expect,400))
        
    def test_function_auto_2(self):
        input = """
        foo : function auto ( a : integer , b : integer ) {}
        a : string = foo(1,2) + 1;
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, StringType, BinExpr(+, FuncCall(foo, [IntegerLit(1), IntegerLit(2)]), IntegerLit(1)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_function_auto_3(self):
        input = """
        foo : function auto () {}
        a : boolean = (foo() :: "string")::foo();
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, BooleanType, BinExpr(::, BinExpr(::, FuncCall(foo, []), StringLit(string)), FuncCall(foo, [])))"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_stmt_call_1(self):
        input = """
        main: function void() {
            a : integer = 0;
            printInteger(a);
            printString(a);
        }
        """
        expect = "Type mismatch in statement: CallStmt(printString, Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_call_2(self):
        input = """
        foo : function auto(a: integer, b: float){
        }
        main: function void() {
            foo(1,2.0);
            res : float = foo(5, 6.1);
            newres : integer = foo(3, 2.0) ;
        }
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(newres, IntegerType, FuncCall(foo, [IntegerLit(3), FloatLit(2.0)]))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_if_1(self):
        input = """
        main: function void() {
            if (1>2) printInteger(a);
        }
        """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_if_2(self):
        input = """
        main: function void() {
            a : boolean = true;
            if (a) { printBoolean(a);}
            else { b: string = a; }
        }
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(b, StringType, Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_for_1(self):
        input = """
        main: function void() {
            i : float ;
            for (i = 1, i <10, i+1) printInteger(i);
        }
        """
        expect = "Type mismatch in statement: ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), IntegerLit(10)), BinExpr(+, Id(i), IntegerLit(1)), CallStmt(printInteger, Id(i)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_for_2(self):
        input = """
        main: function void() {
            i : integer ;
            for (i = 1, i <10, i+1) printInteger("i");
        }
        """
        expect = "Type mismatch in statement: CallStmt(printInteger, StringLit(i))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_for_3(self):
        input = """
        main: function void() {
            i : integer ;
            for (i = 1.0, i <10, i+1) printInteger(i);
        }
        """
        expect = "Type mismatch in statement: ForStmt(AssignStmt(Id(i), FloatLit(1.0)), BinExpr(<, Id(i), IntegerLit(10)), BinExpr(+, Id(i), IntegerLit(1)), CallStmt(printInteger, Id(i)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_while_1(self):
        input = """
        main: function void() {
            a: integer = 0;
            while (false || (a < 3)) {
                a = a + 1;
                printInteger(3.0);
            }
        }
        """
        expect = "Type mismatch in statement: CallStmt(printInteger, FloatLit(3.0))"
        self.assertTrue(TestChecker.test(input,expect,400))
    def test_stmt_dowhile_1(self):
        input = """
        main: function void() {
            a: integer = readInteger();
            b : string ;
            do {
                printInteger(b);
                a = a+1;
            }
            while( (a > 3+1 ) || (7<= 5));
        }
        """
        expect = "Type mismatch in statement: CallStmt(printInteger, Id(b))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_break_1(self):
        input = """
        main: function void() {
            i : integer ;
            for (i = 10, i > 0, i - 2) 
            {
            }
            break;
        }
        """
        expect = "Must in loop: BreakStmt()"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_continue_1(self):
        input = """
        main: function void() {
            i : integer ;
            for (i = 10, i > 0, i - 2) 
            {
            }
            continue;
        }
        """
        expect = "Must in loop: ContinueStmt()"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_return_1(self):
        input = """
        main : function void() {
            a : integer = foo();
            return ;
        }
        toFloat : function float(){
            return 3.0;
        }        
        foo : function integer(){
            return 10.0;
        }
        """
        expect = "Type mismatch in statement: ReturnStmt(FloatLit(10.0))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_(self):
        input = """
        main: function void(){}
        child_function : function integer(a: integer, a: float) inherit parent_function {}
        """
        expect = "Undeclared Function: parent_function"
        self.assertTrue(TestChecker.test(input,expect,400))
    