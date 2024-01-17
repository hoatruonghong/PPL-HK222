import unittest
from TestUtils import TestAST
from AST import *


class ASTGenSuite(unittest.TestCase):
    def test_short_vardecl(self):
        input = """x: integer;"""
        expect = str(Program([VarDecl("x", IntegerType())]))
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_vardecl(self):
        input = """
        x, y, z: integer;
        a: float = 1.2;
        b,c: boolean = true, false;
        d: array[1,2] of boolean;
        e,f: array[2,3] of string;
        g: array[1] of float = {a+1.2};
        h,i: array[1,2] of string = {"D96","MT22"}, {{}, "BKOOL"};
        """
        expect = """Program([
	VarDecl(x, IntegerType)
	VarDecl(y, IntegerType)
	VarDecl(z, IntegerType)
	VarDecl(a, FloatType, FloatLit(1.2))
	VarDecl(b, BooleanType, BooleanLit(True))
	VarDecl(c, BooleanType, BooleanLit(False))
	VarDecl(d, ArrayType([1, 2], BooleanType))
	VarDecl(e, ArrayType([2, 3], StringType))
	VarDecl(f, ArrayType([2, 3], StringType))
	VarDecl(g, ArrayType([1], FloatType), ArrayLit([BinExpr(+, Id(a), FloatLit(1.2))]))
	VarDecl(h, ArrayType([1, 2], StringType), ArrayLit([StringLit(D96), StringLit(MT22)]))
	VarDecl(i, ArrayType([1, 2], StringType), ArrayLit([ArrayLit([]), StringLit(BKOOL)]))
])"""
        self.assertTrue(TestAST.test(input, expect, 301))

    def test_funcdecl(self):
        input = """
        main: function void (){}
        abc: function integer(){}
        def: function integer() inherit abc{}
        ghi: function array[1,2] of boolean () {}
        klm: function array[1,2] of string () inherit ghi {}
        """
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([]))
	FuncDecl(abc, IntegerType, [], None, BlockStmt([]))
	FuncDecl(def, IntegerType, [], abc, BlockStmt([]))
	FuncDecl(ghi, ArrayType([1, 2], BooleanType), [], None, BlockStmt([]))
	FuncDecl(klm, ArrayType([1, 2], StringType), [], ghi, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 302))

    def test_param(self):
        input = """
        abc: function integer(a: integer){}
        def: function integer(a: array[3] of integer) inherit abc{}
        ghi: function array[1,2] of boolean (out n: integer) {}
        klm: function array[1,2] of string (inherit out a: array[3] of integer, n: integer) inherit ghi {}
        """
        expect = """Program([
	FuncDecl(abc, IntegerType, [Param(a, IntegerType)], None, BlockStmt([]))
	FuncDecl(def, IntegerType, [Param(a, ArrayType([3], IntegerType))], abc, BlockStmt([]))
	FuncDecl(ghi, ArrayType([1, 2], BooleanType), [OutParam(n, IntegerType)], None, BlockStmt([]))
	FuncDecl(klm, ArrayType([1, 2], StringType), [InheritOutParam(a, ArrayType([3], IntegerType)), Param(n, IntegerType)], ghi, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 303))

    def test_stmt_1(self):
        input = """
        abs: function integer() {
            return 0;
        }
        main: function void() {
            return;
        }
        """
        expect = """Program([
	FuncDecl(abs, IntegerType, [], None, BlockStmt([ReturnStmt(IntegerLit(0))]))
	FuncDecl(main, VoidType, [], None, BlockStmt([ReturnStmt()]))
])"""
        self.assertTrue(TestAST.test(input, expect, 304))

    def test_stmt_2(self):
        input = """
        plus: function integer(b: integer) {
            a: integer = 2;
            return a + b;
        }
        abs: function integer() inherit plus {
            c: integer = a + plus(5);
            return c;
        }
        """
        expect = """Program([
	FuncDecl(plus, IntegerType, [Param(b, IntegerType)], None, BlockStmt([VarDecl(a, IntegerType, IntegerLit(2)), ReturnStmt(BinExpr(+, Id(a), Id(b)))]))
	FuncDecl(abs, IntegerType, [], plus, BlockStmt([VarDecl(c, IntegerType, BinExpr(+, Id(a), FuncCall(Id(plus), [IntegerLit(5)]))), ReturnStmt(Id(c))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 305))

    def test_stmt_3(self):
        input = """
        modArray: function array[3] of integer (inherit a: array[3] of integer,out n: integer){
            a[0] = a[0] + n;
            if(a[1] < n) a[1] = a[1] + n; 
            if(a[2] > 0) return a;
            else a[2] = -a[2];
            return a;
        }
        """
        expect = """Program([
	FuncDecl(modArray, ArrayType([3], IntegerType), [InheritParam(a, ArrayType([3], IntegerType)), OutParam(n, IntegerType)], None, BlockStmt([AssignStmt(ArrayCell(Id(a), [IntegerLit(0)]), BinExpr(+, ArrayCell(Id(a), [IntegerLit(0)]), Id(n))), IfStmt(BinExpr(<, ArrayCell(Id(a), [IntegerLit(1)]), Id(n)), AssignStmt(ArrayCell(Id(a), [IntegerLit(1)]), BinExpr(+, ArrayCell(Id(a), [IntegerLit(1)]), Id(n)))), IfStmt(BinExpr(>, ArrayCell(Id(a), [IntegerLit(2)]), IntegerLit(0)), ReturnStmt(Id(a)), AssignStmt(ArrayCell(Id(a), [IntegerLit(2)]), UnExpr(-, ArrayCell(Id(a), [IntegerLit(2)])))), ReturnStmt(Id(a))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_4(self):
        input = """
        printArray: function void (inherit a: array[3] of integer,n: integer){
            for(i = 1, i<length(a), i+1) print(a[i]);
            while(a[1]<n) {
                print(a[1]);
                a[1] = a[1] - 1;
            }
            do {
                a[2] = a[2] - n;
            } while(a[2] > 0);
        }
        """
        expect = """Program([
	FuncDecl(printArray, VoidType, [InheritParam(a, ArrayType([3], IntegerType)), Param(n, IntegerType)], None, BlockStmt([ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), FuncCall(Id(length), [Id(a)])), BinExpr(+, Id(i), IntegerLit(1)), CallStmt(print, ArrayCell(Id(a), [Id(i)]))), WhileStmt(BinExpr(<, ArrayCell(Id(a), [IntegerLit(1)]), Id(n)), BlockStmt([CallStmt(print, ArrayCell(Id(a), [IntegerLit(1)])), AssignStmt(ArrayCell(Id(a), [IntegerLit(1)]), BinExpr(-, ArrayCell(Id(a), [IntegerLit(1)]), IntegerLit(1)))])), DoWhileStmt(BinExpr(>, ArrayCell(Id(a), [IntegerLit(2)]), IntegerLit(0)), BlockStmt([AssignStmt(ArrayCell(Id(a), [IntegerLit(2)]), BinExpr(-, ArrayCell(Id(a), [IntegerLit(2)]), Id(n)))]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 307))

    def test_stmt_5(self):
        input = """
        printArray: function void (a: array[3,1] of integer,n: integer){
            while(a[1,1]<n) {
                print(a[1,1]);
                if(n > 1) n = n-1;
                else break;
            }
            {
                m: integer = 5;
                for(i = 1, i<length(a), i+1) {
                    if(a[max(i,2),1]>m) {continue;}
                    else {m = m-1;}
                    m = m + 2;
                }
            }
        }
        """
        expect = """Program([
	FuncDecl(printArray, VoidType, [Param(a, ArrayType([3, 1], IntegerType)), Param(n, IntegerType)], None, BlockStmt([WhileStmt(BinExpr(<, ArrayCell(Id(a), [IntegerLit(1), IntegerLit(1)]), Id(n)), BlockStmt([CallStmt(print, ArrayCell(Id(a), [IntegerLit(1), IntegerLit(1)])), IfStmt(BinExpr(>, Id(n), IntegerLit(1)), AssignStmt(Id(n), BinExpr(-, Id(n), IntegerLit(1))), BreakStmt())])), BlockStmt([VarDecl(m, IntegerType, IntegerLit(5)), ForStmt(AssignStmt(Id(i), IntegerLit(1)), BinExpr(<, Id(i), FuncCall(Id(length), [Id(a)])), BinExpr(+, Id(i), IntegerLit(1)), BlockStmt([IfStmt(BinExpr(>, ArrayCell(Id(a), [FuncCall(Id(max), [Id(i), IntegerLit(2)]), IntegerLit(1)]), Id(m)), BlockStmt([ContinueStmt()]), BlockStmt([AssignStmt(Id(m), BinExpr(-, Id(m), IntegerLit(1)))])), AssignStmt(Id(m), BinExpr(+, Id(m), IntegerLit(2)))]))])]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_short_vardecl(self):
        input = """x: integer;
        """
        expect = str(Program([VarDecl("x", IntegerType())]))
        self.assertTrue(TestAST.test(input, expect, 300))
    def test_short_vardecl2(self):
        input = """x,y,z: integer;
        """
        expect = """Program([
	VarDecl(x, IntegerType)
	VarDecl(y, IntegerType)
	VarDecl(z, IntegerType)
])"""
        self.assertTrue(TestAST.test(input, expect, 320))

    def test_full_vardecl(self):
        input = """x: integer = 1;"""
        expect = """Program([
	VarDecl(x, IntegerType, IntegerLit(1))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_full_vardecl2(self):
        input = """x, y, z: integer = 1, 2, 3;"""
        expect = """Program([
	VarDecl(x, IntegerType, IntegerLit(1))
	VarDecl(y, IntegerType, IntegerLit(2))
	VarDecl(z, IntegerType, IntegerLit(3))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_vardecls(self):
        input = """x, y, z: integer = 1, 2, 3;
        a, b: float;"""
        expect = """Program([
	VarDecl(x, IntegerType, IntegerLit(1))
	VarDecl(y, IntegerType, IntegerLit(2))
	VarDecl(z, IntegerType, IntegerLit(3))
	VarDecl(a, FloatType)
	VarDecl(b, FloatType)
])"""
        self.assertTrue(TestAST.test(input, expect, 302))

    def test_vardecls2(self):
        input = """x , y : boolean = true , false ;
                    a1, a2 : auto = b1, b2 ;"""
        expect = """Program([
	VarDecl(x, BooleanType, BooleanLit(True))
	VarDecl(y, BooleanType, BooleanLit(False))
	VarDecl(a1, AutoType, Id(b1))
	VarDecl(a2, AutoType, Id(b2))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

## Test function declaration

    def test_simple_program(self):
        """Simple program"""
        input = """main: function void () {
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))
    def test_simple_program_2(self):
        """Simple program"""
        input = """main: function integer (a : float) {
        }"""
        expect = """Program([
	FuncDecl(main, IntegerType, [Param(a, FloatType)], None, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))
    def test_simple_program_3(self):
        """Simple program"""
        input = """main: function string (out a : string) {
        }"""
        expect = """Program([
	FuncDecl(main, StringType, [OutParam(a, StringType)], None, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))
    def test_simple_program_4(self):
        """Simple program"""
        input = """Rectangle: function void (a: float, b: integer, out c:float) {
        }
        Square: function void(inherit b: integer) inherit Rectangle{
            
        }
        """
        expect = """Program([
	FuncDecl(Rectangle, VoidType, [Param(a, FloatType), Param(b, IntegerType), OutParam(c, FloatType)], None, BlockStmt([]))
	FuncDecl(Square, VoidType, [InheritParam(b, IntegerType)], Rectangle, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_simple_program_6(self):
        """Simple program"""
        input = """toString : function string () {
        }
        toInteger : function integer () {
        }"""
        expect = """Program([
	FuncDecl(toString, StringType, [], None, BlockStmt([]))
	FuncDecl(toInteger, IntegerType, [], None, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))


# Test expression
    def test_expr_1(self):
        input = """main: function void () {
                a1, b2 : integer = a + 1, 0 ;
                a  = 3;
            }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([VarDecl(a1, IntegerType, BinExpr(+, Id(a), IntegerLit(1))), VarDecl(b2, IntegerType, IntegerLit(0)), AssignStmt(Id(a), IntegerLit(3))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_expr_2(self):
        input = """main: function void () {
                b = a + a1;
                c = b*a/2.0;
            }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(b), BinExpr(+, Id(a), Id(a1))), AssignStmt(Id(c), BinExpr(/, BinExpr(*, Id(b), Id(a)), FloatLit(2.0)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 301))


    def test_expr_3(self):
        input = """
        a : integer = round(1.23-1.496, b);
        """
        expect = """Program([
	VarDecl(a, IntegerType, FuncCall(Id(round), [BinExpr(-, FloatLit(1.23), FloatLit(1.496)), Id(b)]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))


    def test_expr_4(self):
        input = """
        a : float = 12 - 2*3/4 + 1 +1 / 5;
        """
        expect = """Program([
	VarDecl(a, FloatType, BinExpr(+, BinExpr(+, BinExpr(-, IntegerLit(12), BinExpr(/, BinExpr(*, IntegerLit(2), IntegerLit(3)), IntegerLit(4))), IntegerLit(1)), BinExpr(/, IntegerLit(1), IntegerLit(5))))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))


    def test_expr_5(self):
        input = """
                a : float = 2 + 2%2/2*-2 ;
                b : float = 1*1--1+1/1 ;
                c : float = a + b / (2*1.0+1) ;
        """
        expect = """Program([
	VarDecl(a, FloatType, BinExpr(+, IntegerLit(2), BinExpr(*, BinExpr(/, BinExpr(%, IntegerLit(2), IntegerLit(2)), IntegerLit(2)), UnExpr(-, IntegerLit(2)))))
	VarDecl(b, FloatType, BinExpr(+, BinExpr(-, BinExpr(*, IntegerLit(1), IntegerLit(1)), UnExpr(-, IntegerLit(1))), BinExpr(/, IntegerLit(1), IntegerLit(1))))
	VarDecl(c, FloatType, BinExpr(+, Id(a), BinExpr(/, Id(b), BinExpr(+, BinExpr(*, IntegerLit(2), FloatLit(1.0)), IntegerLit(1)))))
])"""
        self.assertTrue(TestAST.test(input, expect, 301))

    def test_expr_6(self):
        input = """
        a : boolean = true ;
        b : boolean = !a && false || (false && true || true) ;  
        c : boolean = !!b || false ;
        """
        expect = """Program([
	VarDecl(a, BooleanType, BooleanLit(True))
	VarDecl(b, BooleanType, BinExpr(||, BinExpr(&&, UnExpr(!, Id(a)), BooleanLit(False)), BinExpr(||, BinExpr(&&, BooleanLit(False), BooleanLit(True)), BooleanLit(True))))
	VarDecl(c, BooleanType, BinExpr(||, UnExpr(!, UnExpr(!, Id(b))), BooleanLit(False)))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_expr_7(self):
        input = """
        a1, a2 : string = "Hello ", "World!" ;
        a: string = a1 :: a2 ;            
        a: string = (a :: ( a :: "a" ) ) :: a;        
        """
        expect = """Program([
	VarDecl(a1, StringType, StringLit(Hello ))
	VarDecl(a2, StringType, StringLit(World!))
	VarDecl(a, StringType, BinExpr(::, Id(a1), Id(a2)))
	VarDecl(a, StringType, BinExpr(::, BinExpr(::, Id(a), BinExpr(::, Id(a), StringLit(a))), Id(a)))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))


    def test_expr_8(self):
        input = """               
        b: boolean = 1!= 2 || (0==0.1) ;       
        """
        expect = """Program([
	VarDecl(b, BooleanType, BinExpr(!=, IntegerLit(1), BinExpr(||, IntegerLit(2), BinExpr(==, IntegerLit(0), FloatLit(0.1)))))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_expr_9(self):
        input = """               
        a : boolean = (3 > 2 ) || (7/2 <= 4+3) && !(1.0e1+1 >= 0) ;     
        """
        expect = """Program([
	VarDecl(a, BooleanType, BinExpr(&&, BinExpr(||, BinExpr(>, IntegerLit(3), IntegerLit(2)), BinExpr(<=, BinExpr(/, IntegerLit(7), IntegerLit(2)), BinExpr(+, IntegerLit(4), IntegerLit(3)))), UnExpr(!, BinExpr(>=, BinExpr(+, FloatLit(10.0), IntegerLit(1)), IntegerLit(0)))))
])"""
        self.assertTrue(TestAST.test(input, expect, 333))


    def test_expr_10(self):
        input = """               
        a : integer = toInt(bc_, 2, 10) + randomInt() ;
        """
        expect = """Program([
	VarDecl(a, IntegerType, BinExpr(+, FuncCall(Id(toInt), [Id(bc_), IntegerLit(2), IntegerLit(10)]), FuncCall(Id(randomInt), [])))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

# # --------- Test array

    def test_array_1(self):
        input = """               
            a : array [2] of integer;
            arr : array [1,2,3] of string;
        """
        expect = """Program([
	VarDecl(a, ArrayType([2], IntegerType))
	VarDecl(arr, ArrayType([1, 2, 3], StringType))
])"""
        self.assertTrue(TestAST.test(input, expect, 310))

    def test_array_2(self):
        input = """               
            arr : array [1_0] of float = {1,2,3,4,5,6,7,8,9,10};
        """
        expect = """Program([
	VarDecl(arr, ArrayType([10], FloatType), ArrayLit([IntegerLit(1), IntegerLit(2), IntegerLit(3), IntegerLit(4), IntegerLit(5), IntegerLit(6), IntegerLit(7), IntegerLit(8), IntegerLit(9), IntegerLit(10)]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_array_3(self):
        input = """               
            value : array[2,3] of float = {{1.2,-4.0e10,1.02*12/1},{a, b, 7.0}};
            S : array[0] of string = {};
        """
        expect = """Program([
	VarDecl(value, ArrayType([2, 3], FloatType), ArrayLit([ArrayLit([FloatLit(1.2), UnExpr(-, FloatLit(40000000000.0)), BinExpr(/, BinExpr(*, FloatLit(1.02), IntegerLit(12)), IntegerLit(1))]), ArrayLit([Id(a), Id(b), FloatLit(7.0)])]))
	VarDecl(S, ArrayType([0], StringType), ArrayLit([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_array_4(self):
        input = """               
            printArr: function void(out arr:array[5] of string) 
                { return (arr[0]);}
            myPets : array[5] of string = {"Cat", "Dog", "Parot", "Pig", "Ducky"} ;    
        """
        expect = """Program([
	FuncDecl(printArr, VoidType, [OutParam(arr, ArrayType([5], StringType))], None, BlockStmt([ReturnStmt(ArrayCell(Id(arr), [IntegerLit(0)]))]))
	VarDecl(myPets, ArrayType([5], StringType), ArrayLit([StringLit(Cat), StringLit(Dog), StringLit(Parot), StringLit(Pig), StringLit(Ducky)]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_array_5(self):
        input = """               
                main : function void(){
                    arrB[0,0,arrB[0,0,arrB[i,i,0]]] = arrayA[10-1,8+1];
                }
        """
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(ArrayCell(Id(arrB), [IntegerLit(0), IntegerLit(0), ArrayCell(Id(arrB), [IntegerLit(0), IntegerLit(0), ArrayCell(Id(arrB), [Id(i), Id(i), IntegerLit(0)])])]), ArrayCell(Id(arrayA), [BinExpr(-, IntegerLit(10), IntegerLit(1)), BinExpr(+, IntegerLit(8), IntegerLit(1))]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))


    def test_array_no(self):
        input = """               
            value : array[2,3] of float = {{1.2,-4.0e10,1.02*12/1},{a, b, 7.0}};
            S : array[0] of string = {};
        """
        expect = """Program([
	VarDecl(value, ArrayType([2, 3], FloatType), ArrayLit([ArrayLit([FloatLit(1.2), UnExpr(-, FloatLit(40000000000.0)), BinExpr(/, BinExpr(*, FloatLit(1.02), IntegerLit(12)), IntegerLit(1))]), ArrayLit([Id(a), Id(b), FloatLit(7.0)])]))
	VarDecl(S, ArrayType([0], StringType), ArrayLit([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 311))



# ## Test statement
# # --------- Assignment
    def test_stmt_assign_1(self):
        input = """
        main: function void () {
                count = 1;
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(count), IntegerLit(1))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_assign_2(self):
        input = """
        average : float = 0.0;
        beginString : string = "";
        main: function void () {
                beginString = "hello world";
                average = sum/number;
        }"""
        expect = """Program([
	VarDecl(average, FloatType, FloatLit(0.0))
	VarDecl(beginString, StringType, StringLit())
	FuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(beginString), StringLit(hello world)), AssignStmt(Id(average), BinExpr(/, Id(sum), Id(number)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_assign_3(self):
        input = """
        count : auto = 0;
        main: function void () {
                
        }"""
        expect = """Program([
	VarDecl(count, AutoType, IntegerLit(0))
	FuncDecl(main, VoidType, [], None, BlockStmt([]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_assign_4(self):
        input = """
        main: function void () {
                count = 1;
                str = "";
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([AssignStmt(Id(count), IntegerLit(1)), AssignStmt(Id(str), StringLit())]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_assign_5(self):
        input = """
        main: function void () {
              r : float = _callR(-1,2.0,a);
              area = pi * r * r;
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([VarDecl(r, FloatType, FuncCall(Id(_callR), [UnExpr(-, IntegerLit(1)), FloatLit(2.0), Id(a)])), AssignStmt(Id(area), BinExpr(*, BinExpr(*, Id(pi), Id(r)), Id(r)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

##---------- If
    def test_stmt_if_1(self):
        input = """
        main: function void () {
              if (a>b) a = b;
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, Id(a), Id(b)), AssignStmt(Id(a), Id(b)))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))
        
    def test_stmt_if_2(self):
        input = """
        main: function void () {
              if (a>b) {a = b;}
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, Id(a), Id(b)), BlockStmt([AssignStmt(Id(a), Id(b))]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_if_3(self):
        input = """
        main: function void () {
              if (a>b) {}
              else {
                print("Value a = ", a);
              }
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, Id(a), Id(b)), BlockStmt([]), BlockStmt([CallStmt(print, StringLit(Value a = ), Id(a))]))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_if_4(self):
        input = """
        main: function void () {
              if (a>b) {}
              else a = "This is 'else' ";                
              
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, Id(a), Id(b)), BlockStmt([]), AssignStmt(Id(a), StringLit(This is 'else' )))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

    def test_stmt_if_5(self):
        input = """
        main: function void () {
              if (a>b) {}
              else if (true) a = b;
                  else a = 0;           
              
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([IfStmt(BinExpr(>, Id(a), Id(b)), BlockStmt([]), IfStmt(BooleanLit(True), AssignStmt(Id(a), Id(b)), AssignStmt(Id(a), IntegerLit(0))))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))

# ## Test full

    def test_more_complex_program(self):
        """More complex program"""
        input = """main: function void () {
            printInteger(4);
        }"""
        expect = """Program([
	FuncDecl(main, VoidType, [], None, BlockStmt([CallStmt(printInteger, IntegerLit(4))]))
])"""
        self.assertTrue(TestAST.test(input, expect, 300))