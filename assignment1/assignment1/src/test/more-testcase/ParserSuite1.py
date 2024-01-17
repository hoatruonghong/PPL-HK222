import unittest
from TestUtils import TestParser


class ParserSuite(unittest.TestCase):
    def test_simple_program_1(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(1);
            }
            printInteger(x);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))

    def test_simple_program_2(self):
        input = """
        main : function void {
            for (i = 1, j < 10, i + 1) {
                writeInt(1);
            }
            printInteger(x);
        }
        """
        expect = "Error on line 2 col 29: {"
        self.assertTrue(TestParser.test(input, expect, 202))

    def test_simple_program_3(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
            }
            printInteger(x);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 203))

    def test_simple_program_4(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
                printInteger(x)
            }
            printInteger(x);
        }
        """
        expect = "Error on line 5 col 12: }"
        self.assertTrue(TestParser.test(input, expect, 204))

    def test_simple_program_5(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(a);
            }
            printInteger();
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 205))

    def test_simple_program_6(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(1);
            }
            printInteger;
        }
        """
        expect = "Error on line 6 col 24: ;"
        self.assertTrue(TestParser.test(input, expect, 206))

    def test_simple_program_7(self):
        input = """
        main : function void() {
            for (i = 1, i + 1) {
                writeInt(1);
            }
            printInteger(x);
        }
        """
        expect = "Error on line 3 col 29: )"
        self.assertTrue(TestParser.test(input, expect, 207))

    def test_simple_program_8(self):
        input = """
        main : void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(1);
            }
            printInteger(x);
        }
        """
        expect = "Error on line 2 col 15: void"
        self.assertTrue(TestParser.test(input, expect, 208))

    def test_simple_program_9(self):
        input = """
        main : function() {
            for (i = 1, j < 10, i + 1) {
                writeInt(1);
            }
            printInteger(x);
        }
        """
        expect = "Error on line 2 col 23: ("
        self.assertTrue(TestParser.test(input, expect, 209))

    def test_simple_program_10(self):
        input = """
        main : function void() {
            for (i = 1, j < 10) {
                writeInt(1);
            }
        }
        """
        expect = "Error on line 3 col 30: )"
        self.assertTrue(TestParser.test(input, expect, 210))
        
    """test if statement"""
    def test_if_statement_11(self):
        input = """
        main : function void() {
            if(true){
                for (i = 1, i < 10, i+1) {
                    writeInt(i);
            }
            }else{
                printInteger(0);
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 211))
        
    def test_if_statement_12(self):
        input = """
        main : function void() {
            if(true){
                for (i = 1, i < 10, i+1) {
                    writeInt(i);
            }
            }else{
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 212))
    def test_if_statement_13(self):
        input = """
        main : function void() {
            if(true){
                for (i = 1, i < 10, i+1) {
                    writeInt(i);
            }
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 213))
    def test_if_statement_14(self):
        input = """
        main : function void() {
            if(true){
            }else{
                printInteger(0);
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 214))
    def test_if_statement_15(self):
        input = """
        fact : function integer(n: integer) {
            if(n==0) return 1;
            else return n*fact(n-1);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))

    """test Variable declarations"""
    def test_var_declarations_16(self):
        input = """
        delta: integer = 3;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 216))
    def test_var_declarations_17(self):
        input = """
        a, b, c: integer = 3, 4, 6;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 217))
    def test_var_declarations_18(self):
        input = """
        a, b, c, d: integer = 3, 4, 6;
        """
        expect = "Error on line 2 col 37: ;"
        self.assertTrue(TestParser.test(input, expect, 218))
    def test_simple_program_8(self):
        input = """
        main : void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(1);
            }
            printInteger(x);
        }
        """
        expect = "Error on line 2 col 15: void"
        self.assertTrue(TestParser.test(input, expect, 210))
    
    
    
    def test_var_declarations_19(self):
        input = """
        x : array [2, 3] of integer
        """
        expect = "Error on line 3 col 8: <EOF>"
        self.assertTrue(TestParser.test(input, expect, 210))
    
    
    def test_var_declarations_20(self):
        input = """
        x : array [2, 3] of float;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 220))
    def test_var_declarations_21(self):
        input = """
        x : array [2, 3, 4, 5] of integer;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 221))
    def test_var_declarations_22(self):
        input = """
        x : auto = 0.0;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 222))
    def test_var_declarations_23(self):
        input = """
        x : auto = 0.0;
        y : auto = true;
        z : auto = "This is a string";
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 223))
    def test_var_declarations_24(self):
        input = """
        x,y,z,y,t,n : auto = 1,2,3,4,5,6;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 224))
    def test_var_declarations_25(self):
        input = """
        x : array [] of integer;
        """
        expect = "Error on line 2 col 19: ]"
        self.assertTrue(TestParser.test(input, expect, 225))
        
    """test expression"""
    def test_expression_26(self):
        input = """
        x : integer = 1+2-3*4/5%-6;
        y : boolean = true ! false && true || false;
        z : string = "This is " :: "a string";
        """
        expect = "Error on line 3 col 27: !"
        self.assertTrue(TestParser.test(input, expect, 226))
    
    def test_error_83(self):
        input = """
        main: function void () {
            x : integer = 1;
            if (x == 1) {
                break;
                return true;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_error_84(self):
        input = """
        main: function void () {
            x : integer = 1;
            if (x == 1) {
                continue;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    
    
    
    
    def test_expression_27(self):
        input = """
        x : boolean = true == false;
        y : boolean = true != false;
        z : boolean = true < false;
        a : boolean = true > false;
        b : boolean = true <= false;
        c : boolean = true >= false;
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 227))
    def test_expression_28(self):
        input = """
        fact : function integer(n: integer) {
            if(n==0) return 1;
            else return n*fact(n-1);
        }
        delta : integer = fact(5);
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 228))
    def test_expression_29(self):
        input = """
        fact : function integer(n: integer) {
            if(n==0) return 1;
            else return n*fact(n-1);
        }
        delta : integer = fact(5)*fact(4)*fact(3);
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 229))
    def test_expression_30(self):
        input = """
        x : integer = a[0, 0];
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 230))
        
    """test assignment statement"""
    def test_assignment_statement_31(self):
        input = """
        main: function void () {
            x : integer;
            x = 1 + 2 + 3;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 231))
    def test_assignment_statement_32(self):
        input = """
        x : array [2, 3] of integer; 
        main: function void () {
            x[1, 2] = 1;
            x[0 ,0] = 2;
            x[0 ,3] = 3;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_assignment_statement_33(self):
        input = """
        x : integer = 1;
        y : integer = 2;
        z : integer;
        main: function void () {
            z = x * y;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 233))
   
   
   
    def test_assignment_statement_34(self):
        input = """
        x,y,z : boolean = true, true, false;
        main: function void () {
            z = x || y && z != x;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 234))
    def test_assignment_statement_35(self):
        input = """
        fact : function integer(n: integer) {
            if(n==0) return 1;
            else return n*fact(n-1);
        }
        main: function void () {
            delta : integer;
            delta = fact(5)*fact(4)*fact(3);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 235))
    def test_assignment_statement_36(self):
        input = """
        fact : function integer(n: integer) {
            if(n==0) return 1;
            else return n*fact(n-1);
        }
        main: function void () {
            delta : integer;
            delta =  -fact(5);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 236))
    def test_assignment_statement_37(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
        }
        delta = inc(5,1);
        """
        expect = "Error on line 5 col 14: ="
        self.assertTrue(TestParser.test(input, expect, 237))
    def test_assignment_statement_38(self):
        input = """
        inc : function integer (out n : integer, delta : integer){
            n = n + delta;
            return n;
        }
        main: function void () {
        delta = inc(5;1);
        }
        """
        expect = "Error on line 7 col 21: ;"
        self.assertTrue(TestParser.test(input, expect, 238))
    def test_assignment_statement_39(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
        }
        main: function void() {
            delta = inc(5,1);
            inc(x, delta);
            printInteger(x);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 239))
    def test_assignment_statement_40(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
        }
        delta : integer == inc(5,1);
        """
        expect = "Error on line 5 col 24: =="
        self.assertTrue(TestParser.test(input, expect, 240))
    
    """test for statement"""
    def test_for_statement_41(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for(i = 1, i < 10, i+1){
                writeInt(i);
            } 
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 241))
    def test_for_statement_42(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for(i = 1, i < 10){
                writeInt(i);
            } 
        }
        """
        expect = "Error on line 5 col 29: )"
        self.assertTrue(TestParser.test(input, expect, 242))
    def test_for_statement_43(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for(i = 1, i+1){
                writeInt(i);
            } 
        }
        """
        expect = "Error on line 5 col 26: )"
        self.assertTrue(TestParser.test(input, expect, 243))
    def test_for_statement_44(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for( i < 10, i+1){
                writeInt(i);
            } 
        }
        """
        expect = "Error on line 5 col 19: <"
        self.assertTrue(TestParser.test(input, expect, 244))
    def test_for_statement_45(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for(i = 1, i < n, i+1){
            } 
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 245))
    def test_for_statement_46(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for(i = 1, i < n, i+1) writeInt(i);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 246))
    def test_for_statement_47(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            i : integer;
            for(i = 1, i < n, i+1){
                delta : integer = 0;
                writeInt(i+delta);
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 247))
    def test_for_statement_48(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            for(){
                
            }
        }
        """
        expect = "Error on line 3 col 16: )"
        self.assertTrue(TestParser.test(input, expect, 248))
    def test_for_statement_49(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            for(i = 1, i < n, i+1){
                return 0;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 249))
    def test_for_statement_50(self):
        input = """
        inc : function void (out n : integer, delta : integer){
            n = n + delta;
            for(i = 1, i < n, i+1){
                return 0;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 250))
        
    """test error"""
    def test_error_81(self):
        input = """
        main: function void () {
            x : integer;
            x = 1 + 2 + 3;
        }
        return 1;
        """
        expect = "Error on line 6 col 8: return"
        self.assertTrue(TestParser.test(input, expect, 281))
    def test_error_82(self):
        input = """
        main: function void () {
            x : integer = 1;
            if (x == 1) {
                return true;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 282))
    def test_error_83(self):
        input = """
        main: function void () {
            x : integer = 1;
            if (x == 1) {
                break;
                return true;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 283))
    def test_error_84(self):
        input = """
        main: function void () {
            x : integer = 1;
            if (x == 1) {
                continue;
            }
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 284))
    def test_error_85(self):
        input = """
        main: function void () {
            
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 285))
    def test_error_86(self):
        input = """
        main: function void () {
            
        }
        return 1;
        """
        expect = "Error on line 5 col 8: return"
        self.assertTrue(TestParser.test(input, expect, 286))
    
    def test_simple_program(self):
        input = """main: function void() {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 203))
    def test_simple_program2(self):
        input = """main: function void() {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    
    def test_simple_program3(self):
        input = """toString: function string(n: integer) {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_simple_program4(self):
        input = """Foo121: function string( out a : integer, b: string) {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_null_program(self):
        input = """ """
        expect = "Error on line 1 col 1: <EOF>"
        self.assertTrue(TestParser.test(input, expect, 201))
        
    #  test simple error of function declaration
    def test_wrong_miss_close1(self):
        input = """func: function void ( {}"""
        expect = "Error on line 1 col 22: {"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_wrong_miss_close2(self):
        input = """func: function int() }"""
        expect = "Error on line 1 col 15: int"
        self.assertTrue(TestParser.test(input, expect, 210))
        
    def test_wrong_miss_functype(self):
        input = """func: function auto ( a: float) {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_wrong_funcname(self):
        input = """2string: function string (n : integer) {}"""
        expect = "Error on line 1 col 0: 2"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_simple_program5(self):
        input = """
        inc : function integer (_n:integer) {}
        delta : function float (out a:string) {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_simple_program5(self):
        input = """
        inc : function integer (_n:integer) {}
        delta : function float (out a:string) {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_simple_program6(self):
        input = """
        multiply : function integer (a:integer, b: integer) {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_simple_program7(self):
        input = """
        _Square_Area  : function float (r: float) inherit Rectangle_Area {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))


    ## test vardecl
    def test_vardecl_(self):
        input = """x : integer = 65 ;"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_vardecl_2(self):
        input = """x,y,z : integer = 65, 12, 30;"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_vardecl_3(self):
        input = """x,y,z : integer = 65, 12, 30, 40;"""
        expect = "Error on line 1 col 28: ,"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_vardecl_4(self):
        input = """True : string = "It's true!" 
        false : string = "it's not true..." """ 
        expect = "Error on line 2 col 8: false"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_vardecl_5(self):
        input = """x , y : boolean = true , false ;
                    a1, a2 : integer = b1, b2 ;""" 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_vardecl_4(self):
        input = """a, b, c, d: auto = 3, 4, 6;""" 
        expect = "Error on line 1 col 26: ;"
        self.assertTrue(TestParser.test(input, expect, 210))

    
    ## expression
    def test_expr_1(self):
        input = """a, b, c, a1: integer = 0;
            main: function void () {
                a1 : integer = a + 1 ;
                b = a + a1;
                c = b-a-10;
            } """ 
        expect = "Error on line 1 col 24: ;"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_expr_2(self):
        input = """main: function void () {
                b = a + a1;
                c = b*a/2.0;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_3(self):
        input = """
            round : function integer(n: float, i: integer){}
            main: function void () {
                a : integer = round(1.23-1.496, b) ;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_4(self):
        input = """
            main: function void () {
                a = 2 + 2%2/2*-2 ;
                b = 1*1--1+1/1 ;
                c = a + b / (2*1.0+1) ;                
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_5(self):
        input = """
            main: function void () {
                a = true ;
                b = !a && false || (false && true || true) ;  
                c = !!b || false ;             
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_6(self):
        input = """
            main: function void () {
                a = b&& c || () ;             
            } """ 
        expect = "Error on line 3 col 30: )"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_7(self):
        input = """
            main: function void () {
                a = b&& c || ;             
            } """ 
        expect = "Error on line 3 col 29: ;"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_8(self):
        input = """
            main: function void () {
                a1, a2 : string = "Hello ", "World!" ;
                a = a1 :: a2 ;            
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_9(self):
        input = """
            main: function void () {
                str : string = "My name ";
                str = str :: "is" :: "Hoa" ;            
            } """ 
        expect = "Error on line 4 col 34: ::"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_5(self):
        input = """
            main: function void () {
                a : boolean ;
                a = (3 > 2 ) || (7/2 <= 4+3) && !(1.0e1+1 >= 0) ;     
                b = 1!= 2 || 0==0.1 ;
            } """ 
        expect = "Error on line 5 col 30: =="
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_expr_6(self):
        input = """
            main: function void () {
                b = 1!= 2 || (0==0.1) ;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    
    
    
    
    
    #-test array type
    def test_array_1(self):
        input = """
            arr : array [2,3] of integer;
            arr_b : array[5] of boolean ;
        """ 
        expect = "successful"
        
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_array_2(self):
        input = """
            value : array[2,3] of float;
            S : array[0] of string;
        """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_array_3(self):
        input = """
                printArr: function void(arr:array[0] of string) { return ;}
                myPets : array[5] of string;
                main : function void(){
                    printAll(myPets);
                }
            """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_array_4(self):
        input = """
                myPets : array[5] of string ;
                main : function void(){
                    myPets [1+1] = myPets [arr[0, nArr[a,c]]-1];
                    myPets[last] = "";
                    printAll(myPets) ;
                }
            """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    
    
    
    ## statement
    def test_stmt_assign_1(self):
        input = """main: function void () {
                r : float = 3.0e4;
                r = 3.01e4 ;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_stmt_assign_2(self):
        input = """
            r : float = 3.0e4;
            r = 3.01e4 ;
            """ 
        expect = "Error on line 3 col 14: ="
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_assign_3(self):
        input = """pi : float = 3.14;
            main: function void () {
                area = 123 ;
                length, width = 3.0, 2;
            } """ 
        expect = "Error on line 4 col 30: ="
        self.assertTrue(TestParser.test(input, expect, 210))
        
    def test_stmt_assign_4(self):
        input = """
            main: function void () {
                area = 123 ;
                length = 3.0, 2;
            } """ 
        expect = "Error on line 4 col 28: ,"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_assign_4(self):
        input = """
            main: function void () {
                area = 123 ;
                length = 3.0, 2;
            } """ 
        expect = "Error on line 4 col 28: ,"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_stmt_if_1(self):
        input = """main: function void () {
                if (a>b) printInteger(a);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_if_2(self):
        input = """main: function void () {
                if (a>b) printInteger(a);
                else printInteger(b);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_if_3(self):
        input = """main: function void () {
                if (a>b) 
                {
                    temp : integer = a;
                    a = b;
                    b = temp ;
                }
                else printInteger(b);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_if_3(self):
        input = """main: function void () {
                if (a>b) 
                else printInteger(b);
            } """ 
        expect = "Error on line 3 col 16: else"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_if_4(self):
        input = """main: function void () {
                if (a>b) printInteger(b)
                
            } """ 
        expect = "Error on line 4 col 12: }"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_if_5(self):
        input = """main: function void () {
                if (a>b) if (true) printString("TRUE"); else printString("FALSE");
                else printInteger(b);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))        
    def test_stmt_if_6(self):
        input = """main: function void () {
                if (a>b) {
                    if (true) printString("TRUE"); 
                }
                else if (a <= 0) printBoolean(value);
                else a = -a;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    
    def test_stmt_for_1(self):
        input = """main: function void () {
                for (i = 1, i <10, i+1) {
                    printInteger(i);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_for_2(self):
        input = """main: function void () {
                for (i = 100, i > 2, i/2) {
                    printFloat(1.0e2);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_3(self):
        input = """main: function void () {
                for (i = n-1, i > 0, i-1) {
                    r : float = a[i] ;                    
                    s = r * r * myPI;
                    printFloat(s);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_4(self):
        input = """main: function void () {
                for (i = n, i != 0, i%2) ;
            } """ 
        expect = "Error on line 2 col 41: ;"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_5(self):
        input = """main: function void () {
                for (i = n, i != 0, i%2) printString("Computer is working...");
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_6(self):
        input = """main: function void () {
                for ( i != 0, i%2) printString("Computer is working...");
            } """ 
        expect = "Error on line 2 col 24: !="
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_7(self):
        input = """main: function void () {
                for (i = n, , i%2) printString("Computer is working...");
            } """ 
        expect = "Error on line 2 col 28: ,"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_8(self):
        input = """main: function void () {
                for (i = n, i != 0, ) printString("Computer is working...");
            } """ 
        expect = "Error on line 2 col 36: )"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_for_9(self):
        input = """main: function void () {
                for (i = n, i != 0, i%2) 
                    a : integer = 0 ;
                    for(j = 0, i < 100, j+a) {
                        a = a + n ;    
                    }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    
    def test_stmt_while_1(self):
        input = """main: function void () {
                while (false) {
                    s = add(2,3,4,5);
                    print(s);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_while_2(self):
        input = """main: function void () {
                while (a > 0 || (b -c < 1)) {
                    printString("printing...");
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_while_3(self):
        input = """main: function void () {
                while () {
                    printString("printing...");
                }
            } """ 
        expect = "Error on line 2 col 23: )"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_while_4(self):
        input = """main: function void () {
                while (false) {
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_while_5(self):
        input = """main: function void () {
                do {
                    a = a - 1; 
                    printInteger(a);
                }
                while(a > 0);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210)) 
    def test_stmt_while_6(self):
        input = """main: function void () {
                do a = a - 1; 
                while(a > 0);
            } """ 
        expect = "Error on line 2 col 19: a"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_while_7(self):
        input = """main: function void () {
                do {
                    if (a == 10) break;
                    a = a - 1; 
                    printInteger(a);
                }
                while(a > 0);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    def test_stmt_while_7(self):
        input = """main: function void () {
                do {
                    if (a == 10) continue;
                    a = a - 1; 
                    printInteger(a);
                }
                while(a > 0);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    
    def test_stmt_break(self):          ### lỗi must reside in a loop 
        input = """
        main : function void() {
            break;
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_continue(self):          ### lỗi must reside in a loop 
        input = """
        main : function void() {
            continue;
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_call_1(self):           
        input = """
        main : function void() {
            foo(2 + x, 4.0 / y);
            goo();
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_call_2(self):           
        input = """
        main : function void() {
            a, b : integer = round(123.0e2), randomInt();
            sum : integer = a + b + arr[0,0];
            print(a, sum);
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))
    def test_stmt_block_1(self):           
        input = """
        main : function void() {
            {
                r, s: integer;
                r = 2.0;
                a, b: array [5] of integer;
                s = r * r * myPI;
                a[0] = s;
            }
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_block_1(self):           
        input = """
        main : function void() {
            {
                {
                    
                }
                if (a == 0) printBoolean(b);
            }
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_block_2(self):           
        input = """
        main : function void() {
            {
                {
                    
                }
                if (a == 0) printBoolean(b);
            }
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_stmt_block_3(self):           
        input = """
        main : function void() {
            {
                a : integer = 5;
                b = a* 2_0 -3 ;
                for (i = b, i > 1 , i-1)
                print(Array[0, i]);
            }
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))    
    def test_stmt_return_1(self):
        input = """
        main: function void() {
            a : string = "Hello world";
            return a::"!";
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 202)) 
    def test_stmt_return_2(self):
        input = """
        main: function void() {
            return a[2,2]*1-b[0]/c;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 202)) 
    def test_stmt_return_3(self):
        input = """
        main: function void() {
            return result+foo(1,2);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 202)) 
    def test_stmt_return_4(self):
        input = """
        main: function void() {
            return ;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201)) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ##test full
    def test_full_1(self):
        input = """
x : integer = 65;
fact : function integer (n : integer) {
    if (n == 0) return 1;
    else return n*fact(n-1);

}
inc : function void (out n: integer, delta: integer){
    n = n + delta ;

}
main : function void () {
    delta : integer = fact(3);
    inc(x, delta);
    printInt(x);
}""" 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 202)) 
    
    
    def test_vardecl_2003(self):
        input = """True : string = "It's true!" 
        false : string = "it's not true..." """
        expect = "Error on line 2 col 8: false"
        self.assertTrue(TestParser.test(input, expect, 2003))
        
        
#################################################
    # def test_full_2(self):
    #     input = """
    #         i : integer ;
    #         f : function integer() {
    #             return 2000;
    #         }
    #         main: function void() {
    #             main : integer ;
    #             main = f();
    #             printInteger(main);
    #             {
    #                 i = readInteger();
    #                 main : integer;
    #                 f : integer;
    #                 main = f = i = 1000;
    #                 printAll(i, main, f) ;
    #             }
    #             return ;
    #         }
    #     """
    #     expect = "Error on line 14 col 29: ="
    #     self.assertTrue(TestParser.test(input, expect, 210)) 
    def test_simple_program_5(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(a);
            }
            printInteger();
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 205))  
    def test_expr_8(self):
        input = """
            main: function void () {
                a1, a2 : string = "Hello ", "World!" ;
                a = a1 :: a2 ;            
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 201))  