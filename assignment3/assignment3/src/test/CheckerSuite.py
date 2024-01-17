import unittest
from TestUtils import TestChecker
from AST import *
# Truong Hong Hoa
# 1911185
from StaticError import *

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
        self.assertTrue(TestChecker.test(input,expect,401))
    
    def test_name_simple_1(self):
        input = """
        main: function void(){
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,402))
    
    def test_name_simple_2(self):
        input = """
        a,b,c,a: integer;
        main: function void(){
        }
        """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,403))
    
    def test_name_simple_3(self):
        input = """
        a: integer;
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,404))
    
    def test_name_simple_5(self):
        input = """
        main: function integer(){}
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,405))
        
    def test_name_simple_6(self):
        input = """
        main: function void(a: integer){}
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,406))
    
    def test_name_simple_7(self):
        input = """
        foo: function integer (){}
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,407))
    
    def test_name_simple_8(self):
        input = """
        foo: function integer (){}
        main: function void(){}
        height, weight : integer;
        foo : integer;
        """
        expect = "Redeclared Variable: foo"
        self.assertTrue(TestChecker.test(input,expect,408))
    
    def test_name_simple_9(self):
        input = """
        main: function void() {
        }
        main: function void() {
        }
        """
        expect = "Redeclared Function: main"
        self.assertTrue(TestChecker.test(input,expect,409))
    
    def test_name_simple_10(self):
        input = """
        main: function void(){}
        height, weight : integer;
        readInteger : integer;
        """
        expect = "Redeclared Variable: readInteger"
        self.assertTrue(TestChecker.test(input,expect,410))
    
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
        self.assertTrue(TestChecker.test(input,expect,412))
    
    def test_array_2(self):
        input = """
        arr : array [3] of integer = {1.0,2.2,3.3};
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(arr, ArrayType([3], IntegerType), ArrayLit([FloatLit(1.0), FloatLit(2.2), FloatLit(3.3)]))"
        self.assertTrue(TestChecker.test(input,expect,413))
    
    def test_array_3(self):
        input = """
        arr : array [2,3,4,5] of integer;
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,414))
    
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

    def test_array_11(self):
        input = """
        arr : array [3,2] of integer = {{1,2}, {3,2}};
        element : integer = arr[arr[0]];
        main: function void(){
        }
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(arr, ArrayType([3, 2], IntegerType), ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(2)])]))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## type mismatch or "undeclared"
    
    ## test funccall
    def test_funccall_1(self):
        input = """
        input : integer = readFloat();
        main: function void(){
        }
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(input, IntegerType, FuncCall(readFloat, []))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_funccall_2(self):
        input = """
        foo : function void() {}
        input : integer = foo();
        main: function void(){
        }
        """
        expect = "Type mismatch in expression: FuncCall(foo, [])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_funccall_3(self):
        input = """
        foo : function float() {}
        input : float = foo(2.0);
        main: function void(){
        }
        """
        expect = "Type mismatch in expression: FuncCall(foo, [FloatLit(2.0)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_funccall_4(self):
        input = """
        foo : function float(a: integer) {}
        input : float = foo(2.0);
        main: function void(){
        }
        """
        expect = "Type mismatch in expression: FuncCall(foo, [FloatLit(2.0)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_funccall_5(self):
        input = """
        foo : function float(a: integer, b: float, c: string, d: boolean) {}
        right_input : float = foo(1,2.0, "String", false);
        wrong_input : float = foo(1,2.0, "String");
        main: function void(){
        }
        """
        expect = "Type mismatch in expression: FuncCall(foo, [IntegerLit(1), FloatLit(2.0), StringLit(String)])"
        self.assertTrue(TestChecker.test(input,expect,400))
        
    def test_funccall_6(self):
        input = """
        a : integer = 1;
        b : float = 2.0 + 3;
        c : string = "Good";
        foo : function float(a: integer, b: float, c: string) {}
        right_input : float = foo(a,b,c);
        wrong_input : float = foo(b,c,a);
        main: function void(){
        }
        """
        expect = "Type mismatch in expression: FuncCall(foo, [Id(b), Id(c), Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,400))
        
    def test_funccall_7(self):
        input = """
        input : integer = _readInteger();
        main: function void(){
        }
        """
        expect = "Undeclared Function: _readInteger"
        self.assertTrue(TestChecker.test(input,expect,400))
        
    def test_funccall_8(self):
        input = """
        round: function integer(number: float){}
        i2f: function float(number: integer){}
        a : float = round(i2f(2)) + 2;
        main: function void(){
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
#     ## test type expression
    def test_id_1(self):
        input = """
        a : integer = 1;
        b : auto = a;
        c : integer = b;
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_id_2(self):
        input = """
        a : integer = 1;
        b : auto = a;
        c : integer = unknown;
        main: function void(){}
        """
        expect = "Undeclared Identifier: unknown"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    
    # def test_id_3(self):
    #     input = """
    #     a : integer = 1;
    #     c : integer = b;
    #     b : auto = a;
    #     main: function void(){}
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    
    # test expr : check - declared -> type
    def test_expr_type_1(self):
        input = """
        a : integer = 3;
        b: integer = a + "halo";
        main: function void(){}
        """
        expect = "Type mismatch in expression: BinExpr(+, Id(a), StringLit(halo))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_expr_type_2(self):
        input = """
        a : string = "3";
        b: string = a + "halo";
        main: function void(){}
        """
        expect = "Type mismatch in expression: BinExpr(+, Id(a), StringLit(halo))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## test stmt
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
    def test_stmt_block_2(self):
        input = """
        a : integer = 1;
        main: function void(){
            a : auto = 2;
            {
                a : auto = 1.2;
            }
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    
    # test function -- typed auto -- suy diễn kiểu cho hàm ở everywhere

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
    
    def test_function_auto_4(self):
        input = """
        toInt : function auto () {}
        toString : function auto(){}
        a : integer = toInt();
        b : string = toString();
        c : auto = toInt() + toString();
        main: function void(){}
        """
        expect = "Type mismatch in expression: BinExpr(+, FuncCall(toInt, []), FuncCall(toString, []))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_function_auto_5(self):
        input = """
        toInt : function auto (a: integer) {}
        toIntInt : function auto(){}
        toFloat: function float () {}
        a : integer = toInt(1);
        b : integer = toIntInt();
        c : auto = toInt(toIntInt()) + toInt(toIntInt()) + toFloat();
        d : integer = c ; 
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(d, IntegerType, Id(c))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_function_auto_6(self):
        input = """
        foo : function auto(){}
        a :  string = (1 > foo()) || false;
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, StringType, BinExpr(||, BinExpr(>, IntegerLit(1), FuncCall(foo, [])), BooleanLit(False)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_function_auto_7(self):
        input = """
        foo : function auto(){}
        a :  string = (2+3 > 5) && foo();
        main: function void(){}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, StringType, BinExpr(&&, BinExpr(>, BinExpr(+, IntegerLit(2), IntegerLit(3)), IntegerLit(5)), FuncCall(foo, [])))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_function_auto_8(self):
        input = """
        foo : function auto(){}
        a : boolean = !foo() == true && false;
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## block stmt
    def test_block_1(self):
        input = """
        main: function void() {
            {
                c : integer = 1;
            }
                b : integer = c;
        }
        """
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_block_2(self):
        input = """
        a : integer = readInteger();
        main: function void() {
            {
                b : integer = 1;
            }
            c : integer = 2;
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_block_3(self):
        input = """
        a : integer = 1;
        main: function void() {
            a : string = "2";
            {
                a: integer = 3;
                {
                    b: float = a;
                }
                b : string = a; 
            }
        }
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(b, StringType, Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ### test assign statement
    def test_stmt_assign_1(self):
        input = """
        a : integer = 1;
        main: function void() {
            b : string ;
            b = "This is a string";
            b = a;
        }
        """
        expect = "Type mismatch in statement: AssignStmt(Id(b), Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_assign_2(self):
        input = """
        foo : function auto (){}
        main: function void() {
            res : auto = readString();
            res = foo();
            res = 1;
        }

        """
        expect = "Type mismatch in statement: AssignStmt(Id(res), IntegerLit(1))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_assign_3(self):
        input = """
        main: function void() {
            a : integer = 2;
            b : float ;
            b = a;
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_assign_4(self):
        input = """
        arr : array [10] of string;
        main: function void() {
            arr[0] = "dog";
            arr = "animal";
        }
        """
        expect = "Type mismatch in statement: AssignStmt(Id(arr), StringLit(animal))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_assign_5(self):
        input = """
        func : function void () {}
        main: function void() {
            func = "";
        }
        """
        expect = "Type mismatch in statement: AssignStmt(Id(func), StringLit())"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_assign_6(self):
        input = """
        main: function void() {
            var = 15;
        }
        """
        expect = "Undeclared Identifier: var"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## test call stmt
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
    
    def test_stmt_call_3(self):
        input = """
        foo : function auto(a: integer, b: float){
        }
        main: function void() {
            foo(5,5.5);
            foo(1);
        }
        """
        expect = "Type mismatch in statement: CallStmt(foo, IntegerLit(1))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_call_4(self):
        input = """
        foo : function auto(a: string, b: integer){
        }
        main: function void() {
            foo("5", 5);
            foo(5, "5");
        }
        """
        expect = "Type mismatch in statement: CallStmt(foo, IntegerLit(5), StringLit(5))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ### test return stmt
    def test_stmt_return_1(self):
        input = """
        foo : function auto () {
            a : integer = 1;
            return 
        }
        main: function void() {
            return ;
        }
        """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,400))
    
    
    ### test if stmt
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
    
    def test_scope_if_1(self):
        input = """
        main: function void(){
            a : integer ;
            if (true) {
                a : float;
            }
            printFloat(a);            
        }
        """
        expect = "Type mismatch in statement: CallStmt(printFloat, Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_scope_if_2(self):
        input = """
        main: function void(){
            a : integer ;
            if (a > 0) printInteger(a);
            
        }
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    

    ## test for stmt
    
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
    
    def test_stmt_for_4(self):
        input = """
        main: function void() {
            i : integer ;
            for (i = 1, i, i+1) printInteger(i);
        }
        """
        expect = "Type mismatch in statement: ForStmt(AssignStmt(Id(i), IntegerLit(1)), Id(i), BinExpr(+, Id(i), IntegerLit(1)), CallStmt(printInteger, Id(i)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_for_5(self):
        input = """
        main: function void() {
            i : integer ;
            for (i = 10, i + 1 > 0, true) printInteger(i);
        }
        """
        expect = "Type mismatch in statement: ForStmt(AssignStmt(Id(i), IntegerLit(10)), BinExpr(>, BinExpr(+, Id(i), IntegerLit(1)), IntegerLit(0)), BooleanLit(True), CallStmt(printInteger, Id(i)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## test while stmt
    
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
    
    def test_stmt_while_2(self):
        input = """
        main: function void() {
            a: integer = readInteger();
            while (a + 3) {
                printInteger(a);
            }
        }
        """
        expect = "Type mismatch in statement: WhileStmt(BinExpr(+, Id(a), IntegerLit(3)), BlockStmt([CallStmt(printInteger, Id(a))]))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_while_3(self):
        input = """
        main: function void() {
            a: integer = readInteger();
            while (a <= 0) {
                a : string = readString();
                a = "Halo";
                while( false) printInteger(a);             
            }
        }
        """
        expect = "Type mismatch in statement: CallStmt(printInteger, Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## test dowhile stmt
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
    
    def test_stmt_dowhile_2(self):
        input = """
        main: function void() {
            a: integer = readInteger();
            b : string ;
            do {
                a = a+1;
            }
            while( b );
        }
        """
        expect = "Type mismatch in statement: DoWhileStmt(Id(b), BlockStmt([AssignStmt(Id(a), BinExpr(+, Id(a), IntegerLit(1)))]))"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_stmt_dowhile_3(self):
        input = """
        a : integer = 1;
        main: function void() {
            do {
                a = a - 1; 
                printInteger(a);
                do {
                    
                } while (a);
            }
            while(a > 0);
        }
        """
        expect = "Type mismatch in statement: DoWhileStmt(Id(a), BlockStmt([]))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
#     ## test break
    
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
    
    def test_stmt_break_2(self):
        input = """
        foo: function void() {
            do {
                while(true) continue;
                if (false) break;
            }
            while(false);
        }
        main: function void(){}
        """
        expect = "Must in loop: BreakStmt()"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## test break
    
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
    
    def test_stmt_continue_2(self):
        input = """
        main: function void() {
            a,b : integer = readInteger(), readInteger();
            i : integer;
            for (i = 1, i <10, i+1) break;
            if (a> b) printInteger(a);
            else continue;
        }
        """
        expect = "Must in loop: ContinueStmt()"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_continue_4(self):
        input = """
        main: function void() {
            while(true) break;
        }
        foo : function void(){
            continue;
        }
        """
        expect = "Must in loop: ContinueStmt()"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    ## test return 
    
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
    
    def test_stmt_return_2(self):
        input = """
        main : function void() {
            printBoolean(isOdd(5));
        }
        isOdd: function boolean(n: integer){
            if (n % 2 == 0) return true;
            else return 0;
        }
        """
        expect = "Type mismatch in statement: ReturnStmt(IntegerLit(0))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_return_4(self):
        input = """
        main : function void() {
            str : string = foo("true");
            {
                break;
            }
        }
        foo: function auto(x: string){
            return "Hello "::x;
        }
        """
        expect = "Must in loop: BreakStmt()"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_stmt_return_5(self):
        input = """
        random: function auto (){
            return  1.0;
        }
        main : function void() {
            showNum(random());
        }
        showNum: function void(a: integer){
            a = a + 1;
            printInteger(a);
        }
        """
        expect = "Type mismatch in statement: CallStmt(showNum, FuncCall(random, []))"
        self.assertTrue(TestChecker.test(input,expect,400))
    def test_decl_order_3(self):
        input = """
        main: function void(){}
        foo : auto = 1;
        foo : function void(){}
        """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    
     
    # ## inheritance
    # # chỉ thừa kế cha, ko thừa kế cha của cha ..

    def test_inherit_1(self):
        input = """
        Shape : function integer(inherit a: float){}
        Rectangle : function integer() inherit Shape {
            preventDefault();
        }
        Square : function integer(a: integer) inherit Rectangle {
            preventDefault();
        }
        main: function void(){}
        Circle : function integer(r: float, a: float) inherit Shape { 
            preventDefault();
        }
        """
        expect = "Invalid Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_2(self):   # liên quan inherit, super đồ đó
        input = """
        foo1: function void (inherit x: integer, inherit y: integer){
            printInteger( x + y) ;
        }
        foo: function void(a :integer) inherit foo1{
            super(a, 3);
        }
        main: function void() {
            x : integer = 2;
            foo(x);
            x : float ;
        }
        """
        expect = "Redeclared Variable: x"
        self.assertTrue(TestChecker.test(input,expect,400))
 
    def test_inherit_4(self):
        input = """
        parent_function : function integer(inherit a: integer, b: float){}
        another_function: function void(){}
        child_function : function integer() inherit parent_function {
            preventDefault();
        }
        main: function void(){}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_6(self):
        input = """
        parent_functions : function integer(a : integer){}
        main: function void(){}
        child_function : function integer(a: integer) inherit parent_function {}
        """
        expect = "Undeclared Function: parent_function"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_7(self):
        input = """
        parent_function : function integer(){}
        main: function void(){}
        child_function : function integer(a: integer) inherit parent_function {}
        """
        expect = "[]"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_8(self):
        input = """
        main: function void(){}
        parent_function : function integer(inherit a: integer){}
        child_function : function integer(a : integer) inherit parent_function {
            super(1);
        }
        """
        expect = "Invalid Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,400)) 
    
#     # def test_inherit_9(self):
#     #     input = """
#     #     parent_function : function integer(inherit a: integer){}
#     #     child_function : function integer(a : integer) inherit parent_function {}
#     #     main: function void(){}
#     #     """
#     #     expect = "Redeclared Parameter: a"
#     #     self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_10(self):
        input = """
        main: function void(){
            child_function(1,1.0);
        }
        parent_function : function integer(inherit a: integer, inherit b: float){}
        child_function : function integer() inherit parent_function {
            super(1, 1.0);
        }
        """
        expect = "Invalid Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,400)) 
    
    def test_inherit_11(self):
        input = """
        a: integer = 2; 
        b: float; 
        bar: function void() inherit foo {
            super(1,2.0);
        } 
        foo: function void(inherit a: integer, b: float) {} 
        b: function void() {} 
        main:function void(){}
        """
        expect = "Redeclared Function: b"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_11(self):
        input = """
        bar: function void() inherit foo {
            preventDefault();
        } 
        foo: function void(inherit a: integer, b: float) {} 
        main:function void() {}
        foo: function void() {}
        """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_12(self):
        input = """
        foo: function void() {}
        main:function void() {}
        foo: function void() inherit foo {
            super();
        }
        """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_inherit_13(self):
        input = """
        main:function void() {}
        foo: function void() inherit foo {
            super();
        }
        """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    # # test nhiều hơn về thừa kế
    
    # def test_inherit_3(self):
    #     input = """
    #     foo: function integer(inherit x: integer) inherit bar
    #     {
    #         super(2);
    #     }
    #     main: function void(){}
    #     bar: function integer(inherit y: integer) inherit foo2 
    #     {
    #         super("Hi");
    #     }
    #     foo2: function integer(inherit z: float) {}
    #     """
    #     expect = "Type mismatch in statement: CallStmt(super, IntegerLit(2))"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    # def test_inherit_12(self):
    #     input = """
    #     a: integer = 2; 
    #     b: auto; 
    #     bar: function void() inherit foo {} 
    #     foo: function void(inherit a: integer, b: float) {} 
    #     b: function void() {} 
    #     main:function void(){}
    #     """
    #     expect = "Invalid Variable: b"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    # def test_inherit_13(self):
    #     input = """
    #     child:function void () inherit parent{
    #     }
    #     main:function void() {
    #     }
    #     parent :function void( inherit a: integer, inherit b:float){
    #     }
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    # def test_super_1(self):
    #     input = """
    #     foo2 : function string() inherit foo{
    #         super(1,1.2);
    #         a = 3;
    #     }
    #     main:function void() {
    #         //preventDefault();
    #     }
    #     foo: function string(inherit a: integer, b: float){}
        
    #     """
    #     expect = "[]"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    # def test_super_2(self):
    #     input = """
    #     parent : function void() {}
    #     child : function void() inherit parent {
    #         a : integer;
    #         preventDefault();
    #     }
    #     main:function void() {
    #     }
        
    #     """
    #     expect = "Sai"
    #     self.assertTrue(TestChecker.test(input,expect,400))
    
    # simple inheritance
        
    def test_super_2(self):
        input = """
        child : function void() inherit parent {
            super(1);
        }
        main:function void() {
        }
        parent : function void(a: integer) {
            super();
        }
        
        """
        expect = "Invalid statement in function: parent"
        self.assertTrue(TestChecker.test(input,expect,400))
     
    def test_super_3(self):
        input = """
        child : function void() inherit parent {
            a : integer;
            super();
        }
        main:function void() {
        }
        parent : function void() {
        }
        
        """
        expect = "Invalid statement in function: child"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_4(self):
        input = """
        child : function void() inherit parent {
            super(1);
        }
        main:function void() {
        }
        parent : function void(a: integer, b: string) {
        }
        
        """
        expect = "Type mismatch in expression: "
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_5(self):
        input = """
        child : function void() inherit parent {
            super(1, 2);
        }
        main:function void() {
        }
        parent : function void(a: integer, b: string) {
        }
        
        """
        expect = "Type mismatch in expression: IntegerLit(2)"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_6(self):
        input = """
        child : function void() inherit parent {
            preventDefault();
            super(1, "hello World");
        }
        main:function void() {
        }
        parent : function void(a: integer, b: string) {
        }
        
        """
        expect = "Invalid statement in function: child"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_7(self):
        input = """
        child : function void() inherit parent {
            super(1, "hello World");
        }
        main:function void() {
        }
        parent : function void(a: integer, b: string, inherit c: float) {
        }
        """
        expect = "Type mismatch in expression: "
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_8(self):
        input = """
        child : function void() inherit parent {
        }
        main:function void() {
            preventDefault();
        }
        parent : function void() {
        }
        """
        expect = "Invalid statement in function: main"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_9(self):
        input = """
        childchild : function void() inherit child {
        }
        child : function void() inherit parent {
        }
        main:function void() {
        }
        parent : function void(a: integer, b: boolean, c: integer) {
        }
        """
        expect = "Invalid statement in function: child"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_9(self):
        input = """
        balloon : integer;
        main: function void() {
            a: string = balloon();
        }
        foo: function void() {}
        """
        expect = "Undeclared Function: balloon"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_10(self):
        input = """
foo: function boolean (inherit a: integer, b: float, c: string) {}

bar: function void(d: float) inherit foo {

        super(12, 2.0);

}
        """
        expect = "Type mismatch in expression: "
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_super_11(self):
        input = """
foo: function boolean (inherit a: integer) {}

bar: function void() inherit foo {

        super(12, 2.0, "hello");

}
        """
        expect = "Type mismatch in expression: FloatLit(2.0)"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_super_9(self):
        input = """
        foo: function void (inherit a: integer, a: float) inherit bar {}
}
        """
        expect = "Undeclared Function: bar"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_param_1(self):
        input = """
        foo: function void (inherit a: integer, a: float) inherit bar {
            x: integer;
            super(1);
        } 
        bar : function void ( m: integer) {}
        main: function void(){}
        """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_scope_1(self):
        input = """
        foo: function void (inherit a: integer) inherit bar {
            b: integer;
            if (a > 0) {
                a: float = 3;
            }
            printFloat(a);
        } 
        bar : function void () {}
        main: function void(){}
        """
        expect = "Type mismatch in statement: CallStmt(printFloat, Id(a))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_undeclare_1(self):
        input = """
        foo: function integer(){}
		a: auto = {1, foo};
        """
        expect = "Undeclared Identifier: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    
    def test_array_auto1(self):
        input = """
		main: function void(){
			a: auto = {1, 2};
			a[1] = 2;

		}
        """
        expect = "Undeclared Identifier: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_redeclared_1(self):
        input = """
		foo : function void(){}
		foo : function integer() inherit bar{}
        """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_redeclared_2(self):
        input = """
		a: integer = 1;

		foo: function void (b : float) inherit a {
			preventDefault();
		}

		a: function string (inherit a: float) {}
        """
        expect = "Redeclared Function: a"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_int_float3(self):
        input = """
		a: auto = 1;
		b: float = a;  
		main: function void(){
			a = 3.0;
		}
        """
        expect = "Type mismatch in statement: AssignStmt(Id(a), FloatLit(3.0))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_auto_param(self):
        input = """
		foo: function void (b: auto, c: auto){
        	a: string = b + c;
        }
		main: function void(){
			
		}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, StringType, BinExpr(+, Id(b), Id(c)))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_auto_param2(self):
        input = """
		foo: function auto (b: auto, c: auto){
        	b = 5;
			c = 5.0;
			return b+c;
        }
		main: function void(){
			b: integer = foo(3,4);
		}
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(b, IntegerType, FuncCall(foo, [IntegerLit(3), IntegerLit(4)]))"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_auto_param3(self):
        input = """
		a: integer = m(1);
		b: integer = m(1.0);
		main: function void () {}
  		m: function integer (b: auto){
			return 1;
		}
        """
        expect = "Type mismatch in expression: FuncCall(m, [FloatLit(1.0)])"
        self.assertTrue(TestChecker.test(input,expect,400))
    