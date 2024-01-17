import unittest
from TestUtils import TestParser


class ParserSuite(unittest.TestCase):
    ## test function prototype
    ## test simple program
    def test_empty(self):
        input = """"""
        expect = "Error on line 1 col 0: <EOF>"
        self.assertTrue(TestParser.test(input, expect, 201))
    def test_simple_program(self):
        input = """main: function void() {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 202))
    def test_simple_program2(self):
        input = """main: function int() {}"""
        expect = "Error on line 1 col 15: int"
        self.assertTrue(TestParser.test(input, expect, 203))    
    def test_simple_program3(self):
        input = """toString: function string(n: integer) {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 204))    
    def test_simple_program4(self):
        input = """Foo121: function string( out a : integer, b: string) {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 205))
        
    ## test simple error of function declaration
    def test_wrong_miss_close1(self):
        input = """func: function void ( {}"""
        expect = "Error on line 1 col 22: {"
        self.assertTrue(TestParser.test(input, expect, 206))
    def test_wrong_miss_close2(self):
        input = """func: function integer() }"""
        expect = "Error on line 1 col 25: }"
        self.assertTrue(TestParser.test(input, expect, 207))
    def test_wrong_miss_functype(self):
        input = """func: function auto ( a: float) {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 208))
    def test_wrong_miss_funcbody(self):
        input = """
        main : function void()"""
        expect = "Error on line 2 col 30: <EOF>"
        self.assertTrue(TestParser.test(input, expect, 209))
    def test_wrong_funcname(self):
        input = """2string: function string (n : integer) {}"""
        expect = "Error on line 1 col 0: 2"
        self.assertTrue(TestParser.test(input, expect, 210))    
    def test_simple_program5(self):
        input = """
        inc : function integer (_n:integer) {}
        delta : function float (out a:string, out b: array[10,10] of integer) {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 211))
    def test_simple_program6(self):
        input = """
        inc : function integer (_n:integer) {}
        delta : function float (out a:string) {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 212))
    def test_simple_program7(self):
        input = """
        multiply : function integer (a:integer, b: boolean) {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 213))
    def test_simple_program8(self):
        input = """
        multiply : function integer (a, b : float,) {}
        main: function void() {}
        """
        expect = "Error on line 2 col 38: ,"
        self.assertTrue(TestParser.test(input, expect, 214))
    def test_simple_program9(self):
        input = """
        _Square_Area  : function float (r: float) inherit Rectangle_Area {}
        main: function void() {}
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 215))
        
    # test vardecl
    def test_vardecl_1(self):
        input = """x : integer = 65 ;"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 216))
    def test_vardecl_2(self):
        input = """x,y,z : integer = 65, 12, 30;"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 217))
    def test_vardecl_3(self):
        input = """True : string = "It's true!" 
        false : string = "it's not true..." """ 
        expect = "Error on line 2 col 8: false"
        self.assertTrue(TestParser.test(input, expect, 218))
    def test_vardecl_4(self):
        input = """x , y : boolean = true , false ;
                    a1, a2 : integer = b1, b2 ;""" 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 219))
    def test_vardecl_5(self):
        input = """
a, b, c, d: auto = 3, 4, 6;
                """ 
        expect = "Error on line 2 col 26: ;"
        self.assertTrue(TestParser.test(input, expect, 220))
    def test_vardecl_6(self):
        input = """
a, b, c: auto = 3, 4, 5, 6;
               """ 
        expect = "Error on line 2 col 23: ,"
        self.assertTrue(TestParser.test(input, expect, 221))
    def test_vardecl_7(self):
        input = """x , y : float ;
                    a1, a2 : float = b1, b2 ;""" 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 222))
    def test_vardecl_8(self):
        input = """x , y : auto ;
                    a1, a2 : string = "a1", "a2", "a3" ;""" 
        expect = "Error on line 2 col 48: ,"
        self.assertTrue(TestParser.test(input, expect, 223))
    def test_vardecl_9(self):
        input = """a1, a2 : void = 1;""" 
        expect = "Error on line 1 col 9: void"
        self.assertTrue(TestParser.test(input, expect, 224))
    def test_vardecl_10(self):
        input = """Integer, float : number = 1,1;""" 
        expect = "Error on line 1 col 9: float"
        self.assertTrue(TestParser.test(input, expect, 225))
    def test_vardecl_11(self):
        input = """a1, a2, a3, a4, a5, a6 : number = 1,1;""" 
        expect = "Error on line 1 col 25: number"
        self.assertTrue(TestParser.test(input, expect, 226))
    def test_vardecl_12(self):
        input = """a1, a2, a3, a4, a5, a6 : integer = 1, 2,3,4, ,;""" 
        expect = "Error on line 1 col 45: ,"
        self.assertTrue(TestParser.test(input, expect, 227))
      
    
    # expression
    def test_expr_1(self):
        input = """a, b, c, a1: integer = 0, 0,0,0;
            main: function void () {
                a1 : integer = a + 1 ;
                b = a + a1;
                c = b-a-10;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 228))
    def test_expr_2(self):
        input = """main: function void () {
                b = a + a1;
                c = b*a/2.0;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 229))
    def test_expr_3(self):
        input = """
            round : function integer(n: float, i: integer){}
            main: function void () {
                a : integer = round(1.23-1.496, b) ;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 230))
    def test_expr_4(self):
        input = """
            main: function void () {
                a = 2 + 2%2/2*-2 ;
                b = 1*1--1+1/1 ;
                c = a + b / (2*1.0+1) ;                
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 231))
    def test_expr_5(self):
        input = """
            main: function void () {
                a = true ;
                b = !a && false || (false && true || true) ;  
                c = !!b || false ;             
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 232))
    def test_expr_6(self):
        input = """
            main: function void () {
                a = b&& c || () ;             
            } """ 
        expect = "Error on line 3 col 30: )"
        self.assertTrue(TestParser.test(input, expect, 233))
    def test_expr_7(self):
        input = """
            main: function void () {
                a = b&& c || ;             
            } """ 
        expect = "Error on line 3 col 29: ;"
        self.assertTrue(TestParser.test(input, expect, 234))
    def test_expr_8(self):
        input = """
            main: function void () {
                a1, a2 : string = "Hello ", "World!" ;
                a = a1 :: a2 ;            
                a = (a :: ( a :: "a" ) ) :: a;
                return a;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 235))
    def test_expr_9(self):
        input = """
            main: function void () {
                str : string = "My name ";
                str = str :: "is" :: "Hoa" ;            
            } """ 
        expect = "Error on line 4 col 34: ::"
        self.assertTrue(TestParser.test(input, expect, 236))
    def test_expr_10(self):
        input = """
            main: function void () {
                a : boolean ;
                a = (3 > 2 ) || (7/2 <= 4+3) && !(1.0e1+1 >= 0) ;     
                b = 1!= 2 || 0==0.1 ;
            } """ 
        expect = "Error on line 5 col 30: =="
        self.assertTrue(TestParser.test(input, expect, 237))
    def test_expr_11(self):
        input = """
            main: function void () {
                b = 1!= 2 || (0==0.1) ;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 238))
    
    ###-test array type
    def test_array_1(self):
        input = """
            arr : array [2,3] of integer;
            arr_b : array[5] of boolean = {true, true, false, false, true};
        """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 239))
    def test_array_2(self):
        input = """
            value : array[2,3] of float = {{1.2,-4.0e10,1.02*12/1},{a, b, 7.0}};
            S : array[0] of string = {};
        """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 240))
    def test_array_3(self):
        input = """
                printArr: function void(out arr:array[5] of string) { printString(arr[0]);}
                myPets : array[5] of string = {"Cat", "Dog", "Parot", "Pig", "Ducky"} ;
                main : function void(){
                    printArr(myPets);
                }
            """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 241))
    def test_array_4(self):
        input = """
                myPets : array[5] of string = {"Cat", "Dog", "Parot", "Pig", "Ducky"} ;
                main : function void(){
                    myPets [1+1] = myPets [arr[0, nArr[a,c]]-1];
                    myPets[last] = "";
                    printAll(myPets) ;
                }
            """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 242))
    def test_array_5(self):
        input = """
                main : function void(){
                    arrayA : array[1_0, 10] of float;
                    arrayB[arrayA[0,0]] = arrayA[10-1,8+1];
                    arrayB : array[] of float;                    
                }
            """ 
        expect = "Error on line 5 col 35: ]"
        self.assertTrue(TestParser.test(input, expect, 243))
    def test_array_6(self):
        input = """
                main : function void(){
                    arrayA : array[1_0, 10_] float;                    
                }
            """ 
        expect = "Error on line 3 col 42: _"
        self.assertTrue(TestParser.test(input, expect, 244))
    def test_array_7(self):
        input = """
                main : function void(){
                    arrayA : array[abc, 2_0] of float;                    
                }
            """ 
        expect = "Error on line 3 col 35: abc"
        self.assertTrue(TestParser.test(input, expect, 245))
    def test_array_8(self):
        input = """
                arrB : array[1_0, 2_0, 3_0_0] of string;                    
                main : function void(){
                    arrB[0,0,arrB[0,0,arrB[i,i,0]]] = readString();
                    return;
                }
            """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 246))
    
    
    
    # statement
    def test_stmt_assign_1(self):
        input = """main: function void () {
                r : float = 3.0e4;
                r = 3.01e4 ;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 247))
    
    def test_stmt_assign_2(self):
        input = """
            r : float = 3.0e4;
            r = 3.01e4 ;
            """ 
        expect = "Error on line 3 col 14: ="
        self.assertTrue(TestParser.test(input, expect, 248))
    def test_stmt_assign_3(self):
        input = """pi : float = 3.14;
            main: function void () {
                area = 123 ;
                length, width = 3.0, 2;
            } """ 
        expect = "Error on line 4 col 30: ="
        self.assertTrue(TestParser.test(input, expect, 249))
    def test_stmt_assign_4(self):
        input = """
            main: function void () {
                area = 123 ;
                length = 3.0, 2;
            } """ 
        expect = "Error on line 4 col 28: ,"
        self.assertTrue(TestParser.test(input, expect, 250))
    def test_stmt_assign_5(self):
        input = """
            pi : float = genPi();
            area = pi * sqr(r);
            main: function void () {
                return;
            } """ 
        expect = "Error on line 3 col 17: ="
        self.assertTrue(TestParser.test(input, expect, 251))
    def test_stmt_assign_6(self):
        input = """
            main: function void () {
              r : float = _readFloat();
              area = pi * sqr(r);
              printFloat("area is ", area);
            } """ 
        expect = "Error on line 5 col 35: ,"
        self.assertTrue(TestParser.test(input, expect, 252))
    def test_stmt_assign_7(self):
        input = """
            main: function void () {
              r : float = readFloat();
              area = pi * sqr(r);
              printFloat("area is ", area);
            } """ 
        expect = "Error on line 3 col 26: readFloat()"
        self.assertTrue(TestParser.test(input, expect, 253))
    
    def test_stmt_if_1(self):
        input = """main: function void () {
                if (a>b) printInteger(a);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 254))
    def test_stmt_if_2(self):
        input = """main: function void () {
                if (a>b) printInteger(a);
                else printInteger(b);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 255))
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
        self.assertTrue(TestParser.test(input, expect, 256))
    def test_stmt_if_4(self):
        input = """main: function void () {
                if (a>b) 
                else printInteger(b);
            } """ 
        expect = "Error on line 3 col 16: else"
        self.assertTrue(TestParser.test(input, expect, 257))
    def test_stmt_if_5(self):
        input = """main: function void () {
                if (a>b) printInteger(b)
                
            } """ 
        expect = "Error on line 4 col 12: }"
        self.assertTrue(TestParser.test(input, expect, 258))
    def test_stmt_if_6(self):
        input = """main: function void () {
                if (a>b) if (true) printString("TRUE"); else printString("FALSE");
                else printInteger(b);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 259))        
    def test_stmt_if_7(self):
        input = """main: function void () {
                if (a>b) {
                    if (true) printString("TRUE"); 
                }
                else if (a <= 0) printBoolean(value);
                else a = -a;
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 260))
    
    def test_stmt_for_1(self):
        input = """main: function void () {
                for (i = 1, i <10, i+1) {
                    printInteger(i);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 261))
    def test_stmt_for_2(self):
        input = """main: function void () {
                for (i = 100, i > 2, i/2) {
                    printFloat(1.0e2);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 262)) 
    def test_stmt_for_3(self):
        input = """main: function void () {
                for (i = n-1, i > 0, i-1) {
                    r : float = a[i] ;                    
                    s = r * r * myPI;
                    printFloat(s);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 263)) 
    def test_stmt_for_4(self):
        input = """main: function void () {
                for (i = n, i != 0, i%2) ;
            } """ 
        expect = "Error on line 2 col 41: ;"
        self.assertTrue(TestParser.test(input, expect, 264)) 
    def test_stmt_for_5(self):
        input = """main: function void () {
                for (i = n, i != 0, i%2) printString("Computer is working...");
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 265)) 
    def test_stmt_for_6(self):
        input = """main: function void () {
                for ( i != 0, i%2) printString("Computer is working...");
            } """ 
        expect = "Error on line 2 col 24: !="
        self.assertTrue(TestParser.test(input, expect, 266)) 
    def test_stmt_for_7(self):
        input = """main: function void () {
                for (i = n, , i%2) printString("Computer is working...");
            } """ 
        expect = "Error on line 2 col 28: ,"
        self.assertTrue(TestParser.test(input, expect, 267)) 
    def test_stmt_for_8(self):
        input = """main: function void () {
                for (i = n, i != 0, ) printString("Computer is working...");
            } """ 
        expect = "Error on line 2 col 36: )"
        self.assertTrue(TestParser.test(input, expect, 268)) 
    def test_stmt_for_9(self):
        input = """main: function void () {
                for (i = n, i != 0, i%2) 
                    a : integer = 0 ;
                    for(j = 0, i < 100, j+a) {
                        a = a + n ;    
                    }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 269)) 
    
    def test_stmt_while_1(self):
        input = """main: function void () {
                while (false) {
                    s = add(2,3,4,5);
                    print(s);
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 270)) 
    def test_stmt_while_2(self):
        input = """main: function void () {
                while (a > 0 || (b -c < 1)) {
                    printString("printing...");
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 271)) 
    def test_stmt_while_3(self):
        input = """main: function void () {
                while () {
                    printString("printing...");
                }
            } """ 
        expect = "Error on line 2 col 23: )"
        self.assertTrue(TestParser.test(input, expect, 272)) 
    def test_stmt_while_4(self):
        input = """main: function void () {
                while (false) {
                }
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 273)) 
    def test_stmt_while_5(self):
        input = """main: function void () {
                do {
                    a = a - 1; 
                    printInteger(a);
                }
                while(a > 0);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 274)) 
    def test_stmt_while_6(self):
        input = """main: function void () {
                do a = a - 1; 
                while(a > 0);
            } """ 
        expect = "Error on line 2 col 19: a"
        self.assertTrue(TestParser.test(input, expect, 275)) 
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
        self.assertTrue(TestParser.test(input, expect, 276)) 
    def test_stmt_while_8(self):
        input = """main: function void () {
                do {
                    if (a == 10) continue;
                    a = a - 1; 
                    printInteger(a);
                }
                while(a > 0);
            } """ 
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 277))     
    def test_stmt_break(self):         
        input = """
        main : function void() {
            printAll();
            break;
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 278))
    def test_stmt_continue(self):         
        input = """
        main : function void() {
            printHelloWorld();
            continue;
            continue_;
            return ;
        }
        """
        expect = "Error on line 5 col 21: ;"
        self.assertTrue(TestParser.test(input, expect, 279))
    def test_stmt_call_1(self):           
        input = """
        main : function void() {
            foo(2 + x, 4.0 / y);
            goo();
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 280))
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
        self.assertTrue(TestParser.test(input, expect, 281))
    def test_stmt_call_3(self):           
        input = """
        main : function void() {
            a : integer = callA() +  1;
            b = _writeInt();
            c : integer = toInteger(sum(a+b)) - min(a,b);
            print(a,b,c);
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 282))
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
        self.assertTrue(TestParser.test(input, expect, 283))
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
        self.assertTrue(TestParser.test(input, expect, 284))
    def test_stmt_block_3(self):           
        input = """
        main : function void() {
            {
                {
                     {
                          printString("Hello World;");
                     }
                }
            }
            return ;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 285))
    def test_stmt_block_4(self):           
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
        self.assertTrue(TestParser.test(input, expect, 286))    
    def test_stmt_return_1(self):
        input = """
        main: function void() {
            a : string = "Hello world";
            return a::"!";
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 287)) 
    def test_stmt_return_2(self):
        input = """
        main: function void() {
            return a[2,2]*1-b[0]/c;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 288)) 
    def test_stmt_return_3(self):
        input = """
        main: function void() {
            return result+foo(1,2);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 289)) 
    def test_stmt_return_4(self):
        input = """
        main: function void() {
            return ;
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 290)) 
        
    
    #test full
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
        self.assertTrue(TestParser.test(input, expect, 291)) 
    
    def test_full_2(self):
        input = """
            i : integer ;
            f : function integer() {
                return 2000;
            }
            main: function void() {
                main : integer ;
                main = f();
                printInteger(main);
                {
                    i = readInteger();
                    main : integer;
                    f : integer;
                    main = f = i = 1000;
                    printAll(i, main, f) ;
                }
                return ;
            }
        """
        expect = "Error on line 14 col 29: ="
        self.assertTrue(TestParser.test(input, expect, 292)) 
    
    def test_full_3(self):
        input = """
            /* Kiem tra mang cap so cong  */
            isEmpty: function boolean (arr: array[10] of integer) {   
                return true;
            }         
            readArray : function void(out arr: array[10] of integer){
                
            }
            isArithmeticProgression: function boolean (arr: array[100] of integer) {
                if (isEmpty(arr)) return false;
                flag : boolean = true;
                i, n, d: integer = 2, len(arr), arr[1]-arr[0];
                
                while (i < n) {
                    if (arr[i]-arr[i-1] != d) flag = false;
                    if (flag == false) return false;
                    i = i +1;
                }
            }
            main:  function void() {
                Array : array [100] of integer;
                readArray(Array);
                if (isArithmeticProgression) printString("This is an arithmetic progression !");
                return;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 293)) 
    def test_full_4(self):
        input = """
            main : function void() {
                year : integer;
                printString("Enter a year: ");
                year = readInteger();
                if (year % 400 == 0) print(year, "is a leap year");
                else if (year % 100 == 0)   print(year, "is not a leap year");
                else if (year % 4 == 0)   print(year, "is a leap year");
                else print(year, "is a leap year");
                return;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 294)) 
        
    def test_full_5(self):
        input = """
            count_occurrences : function integer(out a : array[10] of integer, out x : integer,lo: integer,hi:integer) {
                if( lo > hi) return 0;
                mid: integer = floor((lo+hi)/2);
                if (a[mid] < x) 
                    return count_occurrences(a,x,mid+1,hi);
                else if (a[mid]>x)
                    return count_occurrences(a,x,lo,mid-1);
                else {
                    return 1 + count_occurrences(a,x,lo,mid-1) + count_occurrences(a,x,mid+1,hi);
                    
                } 
            }
            /* in the main function, we call it */
            main: function void() {                
                print(count_occurrences(arr,5,0,len(a)-1));
                return;
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 295)) 
    def test_full_6(self):
        input = """
        main : function void() {
            for (i = 1, j < 10, i + 1) {
                writeInt(a);
            }
            printInteger();
        }
        """
        expect = "Error on line 6 col 25: )"
        self.assertTrue(TestParser.test(input, expect, 296))
    def test_full_7(self):
        input = """
            main : function void() {
                a, b, c, delta, root1, root2, realPart, iPart : float;
                printString("Enter coefficients a, b, c: ");
                a = readFloat();
                b = readFloat();
                c = readFloat();
                delta = b*n - 4*a*c;
                // condition for real and different roots
                if (delta > 0) {
                    root1 = (-b+sqrt(delta))/(2*a);
                    root2 = (-b-sqrt(delta))/(2*a);
                    print("root1 = ", root1," and root2 = ", root2); 
                }
                else if (delta == 0) {
                    root1 = -b/(2*a);
                    root2 = root1;
                    print("root1 = ", root1," and root2 = ", root2);                     
                }
                else // if roots are not real
                {
                    realPart = -b/(2*a);
                    iPart = sqrt(-delta)/(2*a);
                    print("root1 = ", realPart+iPart," and root2 = ",  realPart-iPart);                     
                }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 297)) 
    
    def test_full_8(self):
        input = """
            main : function void() {
                a : integer ;
                a = readInteger();
                printInteger(a);
                b : float = toFloat(a);
                if ((type(b) == "float") && b == a ) {
                    print("Type of b is float.");
                }
                return ;                
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 298)) 
    def test_full_9(self):
        input = """
            main : function void() {
                arr : array[7] of integer = {5, 4, 9, 1, 4, 6, 3 };
                n : integer = sizeof(arr)/sizeof(arr[0]);
                pair1, pair2 : integer;
                if (findPairs(arr, n, pair1, pair2)) {
                    if (checkAnswer(arr, n, pair1, pair2)){
                        printString("Your answer is correct.");                    
                    }
                    else printString("Your answer is incorrect.");
                }
                else printString("No pair found.");
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 299)) 
    def test_full_10(self):
        input = """
            /*Check whether a,b,c are triangle's edges or not
            
            */
            isTriangle: function boolean(a: integer, b:integer, c: integer){
                if ((a+b > c && b+c >a && a+c > b) && a >= 0 || b >=0 || c >= 0 ) return true;
                return false;
            }
            main: function void(){
                if (isTriangle(x,y,z))
                printString("It's a triangle");
                /*
                print if it is not a triangle
                */
            }
        """
        expect = "Error on line 6 col 36: >"
        self.assertTrue(TestParser.test(input, expect, 300)) 
    # def test_full_11(self):
    #     input = """
    #         main : function void() {
    #             x, y : integer = 50, 2;
    #             for(i = 0, i < x , i + y){
    #                 if (i != 3){
    #                     if (arr[i]) {
    #                         print("Hello world");
    #                         y = y + 1;
    #                     }
    #                 }
    #                 else break;
    #             }
    #             print(y);
    #         }
    #     """
    #     expect = "successful"
    #     self.assertTrue(TestParser.test(input, expect, 311)) 
    # def test_full_12(self):
    #     input = """
    #         main : function void() {
    #             print(a[a[a[0]]]);
    #             return; 
    #         }
    #     """
    #     expect = "successful"
    #     self.assertTrue(TestParser.test(input, expect, 212)) 
    # def test_full_13(self):
    #     input = """
    #         fact : function integer(n : integer) {
    #             a = x || y && z != x;
    #             if ((n == 1 )||(n == 0)) return 1;
    #             return n * fact(n-1);
    #         }
    #         main : function void() {
    #             number : integer;
    #             number = readInteger();
    #             printInteger(fact(number));
    #             printInteger(fact(1)*fact(2)*fact(3));
    #             return;
    #         }
    #     """
    #     expect = "successful"
    #     self.assertTrue(TestParser.test(input, expect, 313)) 
    # def test_full_14(self):
    #     input = """
    #         printAnimal : function void() {
                
    #         }
    #         printBird : function void(bird : string) inherit printAnimal {

    #         }
    #         main: function void() {
    #             birds : array[2,3] of string = {{"birdA", "birdB", "birdC"},{"birdX", "birdY", "birdZ"}};
    #             printBird(bird[a[i], 2]);
    #             return ;;
    #         }

    #     """
    #     expect = "Error on line 11 col 24: ;"
    #     self.assertTrue(TestParser.test(input, expect, 214)) 
    # def test_full_15(self):
    #     input = """
    #         main : function void() {
    #             for (i = n,  i >= 0 , i - 1 ){
    #                 printString("Enter value of line "::tostring(i));
    #                 for ( j = 0, j < n, j +1) {
    #                     Print("Enter value of a[",i,",",j,"] : ");
    #                     arr[i,j] = readString();
    #                 }                    
    #             }
    #             print("Length of array arr is ", len(arr));
    #             return;
    #         }
    #     """
    #     expect = "successful"
    #     self.assertTrue(TestParser.test(input, expect, 315)) 
    # def test_full_16(self):
        # input = """
        #     main : function void() {
        #         x = a() + b()*c(d);
        #         if (x < a(arr[0,i])) return;
        #         x = x / max(x,y+sub(x-y));
        #         for (i = 1, i < n , i/2) {
        #             {
        #                 k : integer = 0;
        #                 k = i;
        #                 if (k < 10 ) break;
        #             }
        #         }
        #         print("The result is ",x);
        #     }
        # """
        # expect = "successful"
    #     self.assertTrue(TestParser.test(input, expect, 316)) 
    # def test_full_17(self):
    #     input = """
    #         /*Test associative */
    #         a : float = x * x /2 % 2 +(c% 10)*3.0;
    #         main : function void() {
    #             arr[i, 0] = a[b[x+y[1,2,2,0,0]-h[g[5%2]*t[0,t[1]]] * 8+1--1]] + 3;
    #             b : boolean = 5!=6 && 4+5 > 7 || !(false && false || true);
    #         }
    #     """
    #     expect = "Error on line 6 col 42: >"
    #     self.assertTrue(TestParser.test(input, expect, 317)) 
    # def test_full_18(self):
        # input = """
        #     func : function void(){
        #         ans = 0;
        #         for (i = 1, i <= n  , i + 1) 
        #             for ( j = n, j <i , j -1){
        #                 ans = ans + (i*j*arrayA[i]);
        #             }
        #             print(ans);
        #     }
        #     main: function void(){
        #         func();
        #         return;
        #     }
        # """
    #     expect = "successful"
    #     self.assertTrue(TestParser.test(input, expect, 318)) 
    
    # def test_full_19(self):
    #     input = """
    #         main: function void(){
    #             a : integer =  0;
    #             do printInteger(a);
    #             while (a !=0)
    #             return ;
    #         }
    #     """
    #     expect = "Error on line 4 col 19: printInteger"
    #     self.assertTrue(TestParser.test(input, expect, 319)) 
    # def test_full_20(self):
    #     input = """
    #         {
                
    #         }
    #         main : function void() {
    #             return ;
    #         }
    #     """
    #     expect = "Error on line 2 col 12: {"
    #     self.assertTrue(TestParser.test(input, expect, 320)) 
    
    
    

