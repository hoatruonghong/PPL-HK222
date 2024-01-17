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
        self.assertTrue(TestParser.test(input, expect, 215))

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
    def test_var_declarations_19(self):
        input = """
        x : array [2, 3] of integer
        """
        expect = "Error on line 3 col 8: <EOF>"
        self.assertTrue(TestParser.test(input, expect, 219))
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
        self.assertTrue(TestParser.test(input, expect, 232))
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
        expect = "Error on line 5 col 16: break"
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
        expect = "Error on line 5 col 16: continue"
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
    
    
    