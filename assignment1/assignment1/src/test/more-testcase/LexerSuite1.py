import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):
    
    def test_string_escape3(self):
        self.assertTrue(TestLexer.test(""" "This sentence contains new line\n." """, """Unclosed String: This sentence contains new line\n""", 1007))
    def test_unclosed_string13(self):
        self.assertTrue(TestLexer.test(""" " " "" " """,""" ,,Unclosed String:  """,101))
    def test_unclosed_string14(self):
        self.assertTrue(TestLexer.test("""  "Test \n Unclosed String"  ""","""Unclosed String: Test \n""",101))
    def test_unclosed_string15(self):
        self.assertTrue(TestLexer.test(""" "Test Unclosed String\\" \n" ""","""Unclosed String: Test Unclosed String\\" \n""",101))
    def test_unclosed_string16(self):
        self.assertTrue(TestLexer.test(""" "line 1\\n line 2\n" ""","""Unclosed String: line 1\\n line 2\n""",101))
    def test_unclosed_string17(self):
        self.assertTrue(TestLexer.test(""" "\\"" "'ab'c ""","""\\",Unclosed String: 'ab'c """,101))
    def test_unclosed_string18(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\n"|"|b6783\\")&* ""","""Unclosed String: %^&*(\n""",101))
    def test_unclosed_string19(self):
        self.assertTrue(TestLexer.test(""""\\"Open string""", """Unclosed String: \\"Open string""", 101))
    def test_unclosed_string20(self):
        self.assertTrue(TestLexer.test(""" "Open string \n.\\" """, """Unclosed String: Open string \n""", 303))
    def test_unclosed_string18(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\n"|"|b6783\\")&* ""","""Unclosed String: %^&*(\n""",101))
        # ok
    def test_float11(self):
        self.assertTrue(TestLexer.test(" .2e-3 .E2 .e-22 10.0e-2.2e-3 1. 1.e2 1.2E+10 2.45e-333 0.22 0.e2 23e8 4E 9e-10.34 ",".2e-3,.E2,.e-22,10.0e-2,.2e-3,1.,1.e2,1.2E+10,2.45e-333,0.22,0.e2,23e8,4,E,9e-10,.,34,<EOF>",101))
    def test_integer3(self):
        self.assertTrue(TestLexer.test("123 _123 1_23 123 __123", "123,_123,123,123,__123,<EOF>", 101))
    def test_block_comment7(self):
        self.assertTrue(TestLexer.test("/* This is another block comment / */", "<EOF>", 101))

    def test_1(self):
        """test identifiers"""
        self.assertTrue(TestLexer.test("abc", "abc,<EOF>", 101))
    
    def test_2(self):
        """test comment"""
        self.assertTrue(TestLexer.test(
            """
            //abc
            /* comment */ */            
            """
            , "*,/,<EOF>", 102))

    def test_3(self):
        """intlit floatlit"""
        self.assertTrue(TestLexer.test(
            """
            1234 123
            1_72
            1_234_567
            1.234 1.2e3 7E-10
            1_234.567
            e-10
            """
            , "1234,123,172,1234567,1.234,1.2e3,7E-10,1234.567,e,-,10,<EOF>", 103))

    def test_5(self):
        """intlit floatlit"""
        self.assertTrue(TestLexer.test(
            """
            "This is a string containing tab \t"
            "He asked me: \\"Where is John?\\""
            """
            , """This is a string containing tab \t,He asked me: \\"Where is John?\\",<EOF>""", 105))

    def test_6(self):
        """intlit floatlit"""
        self.assertTrue(TestLexer.test(
            """
            auto break boolean do else
            false float for function if
            integer return string true while
            void out continue of inherit
            array
            """
            , """auto,break,boolean,do,else,false,float,for,function,if,integer,return,string,true,while,void,out,continue,of,inherit,array,<EOF>""", 106))
# test float 11 fails
    def test_7(self):
        """intlit floatlit"""
        self.assertTrue(TestLexer.test(
            """
            + - * / %
            ! && || ==
            != < <= > >=
            ::
            """
            , """+,-,*,/,%,!,&&,||,==,!=,<,<=,>,>=,::,<EOF>""", 107))

    def test_8(self):
        """intlit floatlit"""
        self.assertTrue(TestLexer.test(
            """
            ( ) [ ] . , ; : { } =
            """
            , """(,),[,],.,,,;,:,{,},=,<EOF>""", 108))

    def test_9(self):
        """intlit floatlit"""
        self.assertTrue(TestLexer.test(
            """
            x : integer = 65;
            fact : function integer (n : integer ) {
                if (n == 0) return 1 ;
                else return n * fact (n - 1 ) ;
            }
            inc : function void (out n : integer , delta : integer ) {
                n = n + delta ;
            }
            main : function void () {
                delta : integer = fact (3) ;
                inc(x,delta) ;
                printInteger(x) ;
            }
            """
            , """x,:,integer,=,65,;,fact,:,function,integer,(,n,:,integer,),{,if,(,n,==,0,),return,1,;,else,return,n,*,fact,(,n,-,1,),;,},inc,:,function,void,(,out,n,:,integer,,,delta,:,integer,),{,n,=,n,+,delta,;,},main,:,function,void,(,),{,delta,:,integer,=,fact,(,3,),;,inc,(,x,,,delta,),;,printInteger,(,x,),;,},<EOF>""", 109))

    def test_10(self):
        """test comment"""
        self.assertTrue(TestLexer.test(
            """
            //abc
            /* commemts */
            // eof
            """
            , "<EOF>", 110))
    
    def test_11(self):
        """test comment"""
        self.assertTrue(TestLexer.test(
            """
            {1, 5, 7, 12} {"Kangxi", "Yongzheng", "Qianlong"}
            """
            , "{,1,,,5,,,7,,,12,},{,Kangxi,,,Yongzheng,,,Qianlong,},<EOF>", 111))

    def test_12(self):
        """test comment"""
        self.assertTrue(TestLexer.test(
            """
            x : array [2, 3] of integer;
            fact : function integer (n : integer ) {
                for (i = 1, i < 10, i + 1) {
                    writeInt(i);
                }
            }
            main : function void () {
                r, s: integer;
                r = 2.0;
                a, b: array [5] of integer;
                s = r * r * myPI;
                a[0] = s;
            }
            """
            , "x,:,array,[,2,,,3,],of,integer,;,fact,:,function,integer,(,n,:,integer,),{,for,(,i,=,1,,,i,<,10,,,i,+,1,),{,writeInt,(,i,),;,},},main,:,function,void,(,),{,r,,,s,:,integer,;,r,=,2.0,;,a,,,b,:,array,[,5,],of,integer,;,s,=,r,*,r,*,myPI,;,a,[,0,],=,s,;,},<EOF>", 112))

    def test_inline_comment(self):
        self.assertTrue(TestLexer.test("// This is a comment", "<EOF>", 101))
    def test_inline_comment2(self):
        self.assertTrue(TestLexer.test("// This is a comment \n", "<EOF>", 101))
    def test_inline_comment3(self):
        self.assertTrue(TestLexer.test("// This is a comment with \"\\\" inside.", "<EOF>", 101))
    def test_inline_comment4(self):
        self.assertTrue(TestLexer.test("//*This is still a inline comment", "<EOF>", 101))
    def test_inline_comment5(self):
        self.assertTrue(TestLexer.test("//*This is still a inline comment*/", "<EOF>", 101))
    def test_block_comment1(self):
        self.assertTrue(TestLexer.test("/* This is a block comment */", "<EOF>", 102))
    def test_block_comment2(self):
        self.assertTrue(TestLexer.test("/* This is a block comment \nwith multiple lines */", "<EOF>", 102))
    def test_block_comment3(self):
        self.assertTrue(TestLexer.test("/* This is a block //comment */", "<EOF>", 102))
    def test_block_comment4(self):
        self.assertTrue(TestLexer.test("/* This is a block comment end with \"* /\" */", "<EOF>", 102))
    def test_block_comment5(self):
        self.assertTrue(TestLexer.test("/* This is a block comment \n//Inline Comment */", "<EOF>", 102))
    def test_block_comment6(self):
        self.assertTrue(TestLexer.test("/* This is a unclose block comment ", "/,*,This,is,a,unclose,block,comment,<EOF>", 102))
    def test_block_comment7(self):
        self.assertTrue(TestLexer.test("/* This is another block comment */ */", "*,/,<EOF>", 101))
    def test_nested_comment1(self):
        self.assertTrue(TestLexer.test("// A line comment // contains another line comment . ", "<EOF>", 101))
    def test_nested_comment2(self):
        self.assertTrue(TestLexer.test("/*a block cmt /*cover a block cmt*/ */ ", "*,/,<EOF>", 101))
    def test_nested_comment3(self):
        self.assertTrue(TestLexer.test("/*block comment 1*/\n/*block comment2*///inline comment", "<EOF>", 101))
    
    def test_identifier(self):
        self.assertTrue(TestLexer.test("my name is Hoa", "my,name,is,Hoa,<EOF>", 101))
    def test_identifier2(self):
        self.assertTrue(TestLexer.test("__", "__,<EOF>", 101))
    def test_identifier3(self):
        self.assertTrue(TestLexer.test("Ident 1 id1", "Ident,1,id1,<EOF>", 101))
    def test_identifier4(self):
        self.assertTrue(TestLexer.test("1Cat+2_Dogs", "1,Cat,+,2,_Dogs,<EOF>", 101))
    def test_identifier4(self):
        self.assertTrue(TestLexer.test("X/123", "X,/,123,<EOF>", 101))
    def test_identifier5(self):
        self.assertTrue(TestLexer.test("_count 123number||sum", "_count,123,number,||,sum,<EOF>", 101))
    def test_identifier6(self):
        self.assertTrue(TestLexer.test("1day, I go to _school123_.;", "1,day,,,I,go,to,_school123_,.,;,<EOF>", 101))
     
    def test_keyword1(self):
        self.assertTrue(TestLexer.test("autobreakboolean", "autobreakboolean,<EOF>", 101))
    def test_keyword2(self):
        self.assertTrue(TestLexer.test("integer function void", "integer,function,void,<EOF>", 101))
        # ok
    def test_integer1(self):
        self.assertTrue(TestLexer.test("0090", "0,0,90,<EOF>", 101))
    def test_integer2(self):
        self.assertTrue(TestLexer.test("-090x90", "-,0,90,x90,<EOF>", 101))
    def test_integer3(self):
        self.assertTrue(TestLexer.test("123 _123 1_23 123_ __123", "123,_123,123,123,__123,<EOF>", 101))
    def test_integer4(self):
        self.assertTrue(TestLexer.test("123*901/10", "123,*,901,/,10,<EOF>", 101))
    def test_integer5(self):
        self.assertTrue(TestLexer.test("1_23__456_", "123456,_,<EOF>", 1099)) ## __ với chỉ số ở thập phân
#        self.assertTrue(TestLexer.test("1_23__456_", "123,__456_,<EOF>", 101)) ## __ với chỉ số ở thập phân
    def test_integer6(self):
        self.assertTrue(TestLexer.test("5 + 100/20", "5,+,100,/,20,<EOF>", 101))
    def test_integer7(self):
        self.assertTrue(TestLexer.test("-1000-10+-100/1", "-,1000,-,10,+,-,100,/,1,<EOF>", 101))
    def test_integer8(self):
        self.assertTrue(TestLexer.test("80 < 120 && (3-7) >= 7", "80,<,120,&&,(,3,-,7,),>=,7,<EOF>", 101))
    def test_integer9(self):
        self.assertTrue(TestLexer.test("5!=8 || 12%4 == 0", "5,!=,8,||,12,%,4,==,0,<EOF>", 101))
    def test_integer10(self):
        self.assertTrue(TestLexer.test("x00_0 010 1000x", "x00_0,0,10,1000,x,<EOF>", 101))
    # ok
    def test_float1(self):
        self.assertTrue(TestLexer.test("1.2e10", "1.2e10,<EOF>", 101))
    def test_float2(self):
        self.assertTrue(TestLexer.test(" 7.5 0.6 ", "7.5,0.6,<EOF>", 101))
    def test_float3(self):
        self.assertTrue(TestLexer.test(" 5.1+1e5 ","5.1,+,1e5,<EOF>",101))
    def test_float4(self):
        self.assertTrue(TestLexer.test(" 6.8+9.2 ","6.8,+,9.2,<EOF>",101))
    def test_float5(self):
        self.assertTrue(TestLexer.test(" -1.3+1e3 ","-,1.3,+,1e3,<EOF>",101))
    def test_float6(self):
        self.assertTrue(TestLexer.test(" .6 ",".,6,<EOF>",101))
    def test_float7(self):
        self.assertTrue(TestLexer.test(" 7E15 ","7E15,<EOF>",101))
    def test_float8(self):
        self.assertTrue(TestLexer.test(" 1.0e ","1.0,e,<EOF>",101))
    def test_float9(self):
        self.assertTrue(TestLexer.test("4.1e3 ","4.1e3,<EOF>",101))
    def test_float10(self):
        self.assertTrue(TestLexer.test(" 5e-8+6 ","5e-8,+,6,<EOF>",101))
    def test_float11(self):
        self.assertTrue(TestLexer.test(" 10.0e-2.2e-3 ","10.0e-2,.2e-3,<EOF>",101))
   # ok
    def test_string(self):
        self.assertTrue(TestLexer.test(""""Hello World !" ""","""Hello World !,<EOF>""",101))
    def test_string2(self):
        self.assertTrue(TestLexer.test(""""1 Cat + 2 Dogs :: 12 Birds, 3 Spiders in the picture." ""","""1 Cat + 2 Dogs :: 12 Birds, 3 Spiders in the picture.,<EOF>""",101))
    def test_string3(self):
        self.assertTrue(TestLexer.test(""""Hello World !\"\n\"The result is: \"2 ""","""Hello World !,The result is: ,2,<EOF>""",101))
    def test_string4(self):
        self.assertTrue(TestLexer.test(""""abc" ""","""abc,<EOF>""",101))
    def test_string9(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\t"|"|b6783\\")&* ""","""%^&*(	,Error Token |""",101))
    
    def test_string_comment(self):
        self.assertTrue(TestLexer.test(""" "Hello /*My*/ World" ""","""Hello /*My*/ World,<EOF>""",101))
    ## chỗ này có lỗi ko? nếu có là unclosed string hay error token # 
    def test_string_comment2(self):
        self.assertTrue(TestLexer.test(""" "Hello World/* " */  ""","""Hello World/* ,*,/,<EOF>""",101))
    def test_string_comment3(self):
        self.assertTrue(TestLexer.test(""" "Hello //My World" ""","""Hello //My World,<EOF>""",101))
    # ok
    def test_string_escape(self):
        self.assertTrue(TestLexer.test(""""This is a string containing tab \t." """, """This is a string containing tab \t.,<EOF>""", 101))
    def test_string_escape2(self):
        self.assertTrue(TestLexer.test(""""He asked me: \"Where is John?\"" """, """He asked me: \"Where is John?\",<EOF>""", 101))
    ## He asked me: "Where is John?" lồng string trong string
    def test_string_escape3(self):
        self.assertTrue(TestLexer.test(""""This sentence contains new line\n." """, """Unclosed String: \"This sentence contains new line""", 101))
    def test_string_escape4(self):
        self.assertTrue(TestLexer.test(""""Print it ( a line char \\n )" """, """Print it ( a line char \\n ),<EOF>""", 101))
    def test_string_escape5(self):
        self.assertTrue(TestLexer.test(""""There is a backspace \b. before here." """, """There is a backspace \b. before here.,<EOF>""", 101))
    def test_string_escape6(self):
        self.assertTrue(TestLexer.test(""""Multiple chars \\\\" """, """Multiple chars \\\\,<EOF>""", 1067))
    def test_string_escape7(self):
        self.assertTrue(TestLexer.test(""""He asked me: \\"Where is John?\\"" """, """He asked me: \\"Where is John?\\",<EOF>""", 101))
    def test_string_escape8(self):
        self.assertTrue(TestLexer.test("""" Print integer number by \"printInt(anArg: int)\"" """, """ Print integer number by ,printInt,(,anArg,:,int,),,<EOF>""", 1001))
    def test_string_escape9(self):
        self.assertTrue(TestLexer.test(""""We combine \' \f. \t. \'" """, """We combine \' \f. \t. \',<EOF>""", 101))
    def test_string_escape10(self):
        self.assertTrue(TestLexer.test(""""This is a string containing /*comment*/" """, """This is a string containing /*comment*/,<EOF>""", 101))
    def test_string_escape11(self):
        self.assertTrue(TestLexer.test(""""He said: \'He said:\'I saw him.\'\'" """, """He said: \'He said:\'I saw him.\'\',<EOF>""", 101))
    def test_string_escape12(self):
        self.assertTrue(TestLexer.test(""""He said: \\"He said:\\"I saw him.\\"\\"" """, """He said: \\"He said:\\"I saw him.\\"\\",<EOF>""", 1000))
    def test_unclosed_string13(self):
        self.assertTrue(TestLexer.test(""" " " "" " """,""" ,,Unclosed String:  """,101))
    def test_unclosed_string14(self):
        self.assertTrue(TestLexer.test("""  "Test \n Unclosed String"  ""","""Unclosed String: Test """,101))
    def test_unclosed_string15(self):
        self.assertTrue(TestLexer.test(""" "Test Unclosed String\\" \n" ""","""Unclosed String: Test Unclosed String\\" """,1066))
    def test_unclosed_string16(self):
        self.assertTrue(TestLexer.test(""" "line 1\\n line 2\n" ""","""Unclosed String: line 1\\n line 2""",101))
    def test_unclosed_string17(self):
        self.assertTrue(TestLexer.test(""" "\\"" "'ab'c ""","""\\",Unclosed String: 'ab'c """,101))
    def test_unclosed_string18(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\n"|"|b6783\\")&* ""","""Unclosed String: %^&*(""",101))
    def test_unclosed_string19(self):
        self.assertTrue(TestLexer.test(""""\\"Open string""", """Unclosed String: \\"Open string""", 101))
    def test_unclosed_string20(self):
        self.assertTrue(TestLexer.test(""" "Open string \n.\\" """, """Unclosed String: Open string """, 303))
    ## xem lại 
    def test_illegal_string4(self):
        self.assertTrue(TestLexer.test("""  "abc123a\\mabc"  ""","""Illegal Escape In String: abc123a\\m""",301))
    def test_illegal_string5(self):
        self.assertTrue(TestLexer.test("""   123-4"abc123a\\b\\iasVm"  ""","""123,-,4,Illegal Escape In String: abc123a\\b\\i""",302))
    def test_illegal_string6(self):
        self.assertTrue(TestLexer.test("""  "Hi, this is abc \\h\\n\\t "  ""","""Illegal Escape In String: Hi, this is abc \h""",303))
    def test_illegal_string7(self):
        self.assertTrue(TestLexer.test(""" "     " " " "" "\\t\\b\\g" ""","""     , ,,Illegal Escape In String: \\t\\b\\g""",304))
    def test_illegal_string8(self):
        self.assertTrue(TestLexer.test(""" "X=004*0875.E-2\\087.02" ""","""Illegal Escape In String: X=004*0875.E-2\\0""",305))
    def test_illegal_string9(self):
        self.assertTrue(TestLexer.test(""" "illegal_escape\" ""","""illegal_escape,<EOF>""",306))
    def test_illegal_string10(self):
        self.assertTrue(TestLexer.test(""" 
        "t \ {abcd}\\efg"
        ""","Illegal Escape In String: t \ ",101))
    def test_operator(self):
        self.assertTrue(TestLexer.test("+ - * / ! % || && != == <= >= > < =", "+,-,*,/,!,%,||,&&,!=,==,<=,>=,>,<,=,<EOF>", 101))
    def test_operator2(self):
        self.assertTrue(TestLexer.test("2*2 + 2^ 1", "2,*,2,+,2,Error Token ^", 101))
    def test_operator3(self):
        self.assertTrue(TestLexer.test("do {print(a);} while (a & b);", "do,{,print,(,a,),;,},while,(,a,Error Token &", 101))
    def test_operator4(self):
        self.assertTrue(TestLexer.test("income=income + salary*1.2*rate[1]+month#3;", "income,=,income,+,salary,*,1.2,*,rate,[,1,],+,month,Error Token #", 101))
    def test_operator5(self):
        self.assertTrue(TestLexer.test("cost = sum((y-h(i))**2)", "cost,=,sum,(,(,y,-,h,(,i,),),*,*,2,),<EOF>", 101))
    def test_operator6(self):
        self.assertTrue(TestLexer.test("x = (4 + 3i)(2 + 5i).i^2", "x,=,(,4,+,3,i,),(,2,+,5,i,),.,i,Error Token ^", 101))
    def test_operator7(self):
        self.assertTrue(TestLexer.test("+-*/%*()/*//$#", "+,-,*,/,%,*,(,),/,*,<EOF>", 101))

    def test_separators(self):
        self.assertTrue(TestLexer.test("(  ) [ ] { } ; ,  =", "(,),[,],{,},;,,,=,<EOF>", 101))
    
    def test_full1(self):
        self.assertTrue(TestLexer.test("array[1+2,0]=0;","array,[,1,+,2,,,0,],=,0,;,<EOF>",101))
    def test_full2(self):
        self.assertTrue(TestLexer.test("x,y,z: float = 1.20e10, 7E-2, 3*a","x,,,y,,,z,:,float,=,1.20e10,,,7E-2,,,3,*,a,<EOF>",101))
    def test_full3(self):
        self.assertTrue(TestLexer.test("20>>3<<4<===>=b","20,>,>,3,<,<,4,<=,==,>=,b,<EOF>",101))
    def test_full4(self):
        self.assertTrue(TestLexer.test("(2.2+03)||a!==3&a","(,2.2,+,0,3,),||,a,!=,=,3,Error Token &",101))
    def test_full5(self):
        self.assertTrue(TestLexer.test("super(a[0,0],b*c-d,+3.4e-1+.e-2);","super,(,a,[,0,,,0,],,,b,*,c,-,d,,,+,3.4e-1,+,.e-2,),;,<EOF>",101)) 
    
    def test_float10(self): 
        self.assertTrue(TestLexer.test("0.e-11 1.2E-22 0E 00.e .0e1 .0e-1","0.e-11,1.2E-22,0,E,0,0.,e,.0e1,.0e-1,<EOF>",101))   
    def test_string_escape2(self):
        self.assertTrue(TestLexer.test(""""He asked me: \\"Where is John?\\"" """, """He asked me: \\"Where is John?\\",<EOF>""", 151))
    ## He asked me: "Where is John?" lồng string trong string
    def test_string_escape3(self):
        self.assertTrue(TestLexer.test("""
        "This sentence contains new line
        "
        """, """Unclosed String: This sentence contains new line""", 152))
    def test_statement1(self):
        self.assertTrue(TestLexer.test("a:string =\"Hello, World!\n\"","a,:,string,=,Unclosed String: Hello, World!",101))  # xem lại
    def test_statement2(self):
        self.assertTrue(TestLexer.test("printInteger(123);","printInteger,(,123,),;,<EOF>", 101)) 
    def test_statement3(self):
        self.assertTrue(TestLexer.test("arr: array[1,2] of integer = {{-1,2}};","arr,:,array,[,1,,,2,],of,integer,=,{,{,-,1,,,2,},},;,<EOF>", 101)) 
    def test_statement3(self):
        self.assertTrue(TestLexer.test("printInteger(123);","printInteger,(,123,),;,<EOF>", 101)) 
    def test_program_1(self):
        self.assertTrue(TestLexer.test("""
main : function void() {                                      
    printString("Hello World");
    return ;
}
""", "main,:,function,void,(,),{,printString,(,Hello World,),;,return,;,},<EOF>",101))
    def test_program_2(self):
        self.assertTrue(TestLexer.test("""
main : function void() {                                       
// first block
{
    // second block
    {
        // third block
        {
            // fourth block
        }
    }
}}""", "main,:,function,void,(,),{,{,{,{,},},},},<EOF>",101))
    def test_program_3(self):
        self.assertTrue(TestLexer.test("""
a : integer = 0;
main : function void() {                                      
    return a;
}
""", "a,:,integer,=,0,;,main,:,function,void,(,),{,return,a,;,},<EOF>",101))
    def test_program_4(self):
        self.assertTrue(TestLexer.test("""
a : integer = 0;
main : function void() {                                      
    return a;
}
""", "a,:,integer,=,0,;,main,:,function,void,(,),{,return,a,;,},<EOF>",101))
    def test_program_5(self):
        self.assertTrue(TestLexer.test("""
{
r, s: integer;
r = 2.0;
a, b: array [5] of integer;
s = r * r * myPI;
a[0] = s;
}
""", "{,r,,,s,:,integer,;,r,=,2.0,;,a,,,b,:,array,[,5,],of,integer,;,s,=,r,*,r,*,myPI,;,a,[,0,],=,s,;,},<EOF>",101))
    def test_program_6(self):
        self.assertTrue(TestLexer.test("""
main: function void () {
    if (a>b) if (true) printString("TRUE"); else printString("FALSE");
    else printInteger(b);
    return;
}
""", "main,:,function,void,(,),{,if,(,a,>,b,),if,(,true,),printString,(,TRUE,),;,else,printString,(,FALSE,),;,else,printInteger,(,b,),;,return,;,},<EOF>",101))
    def test_program_7(self):
        self.assertTrue(TestLexer.test("""
main: function void () {
    for (i = n, , i%2) printString("Computer is working...\n");
}
""", "main,:,function,void,(,),{,for,(,i,=,n,,,,,i,%,2,),printString,(,Unclosed String: Computer is working...",1088))
    def test_program_8(self):
        self.assertTrue(TestLexer.test("""
            main: function void () {
                do {
                    if (a == 10) break;
                    a = a - 1; 
                    printInteger(a);
                }
                while(a > 0);
            }
""", "main,:,function,void,(,),{,do,{,if,(,a,==,10,),break,;,a,=,a,-,1,;,printInteger,(,a,),;,},while,(,a,>,0,),;,},<EOF>",101))
    def test_program_9(self):
        self.assertTrue(TestLexer.test("""
            main : function void() {
                a, b : integer = round(123.0e2), randomInt();
                /*
                Calculate sum of 2 numbers a & b
                */
                sum : integer = a + b + arr[0,0];
                print(a, sum);
                return ;
            }
""", "main,:,function,void,(,),{,a,,,b,:,integer,=,round,(,123.0e2,),,,randomInt,(,),;,sum,:,integer,=,a,+,b,+,arr,[,0,,,0,],;,print,(,a,,,sum,),;,return,;,},<EOF>",101))
    def test_program_10(self):
        self.assertTrue(TestLexer.test("""
            main: function void() {
                a : string = "Hello world"; // string 
                return a::"!";
            }  
""", "main,:,function,void,(,),{,a,:,string,=,Hello world,;,return,a,::,!,;,},<EOF>",101))
    def test_program_11(self):
        self.assertTrue(TestLexer.test("""
            main : function void() {
            foo(2__0 + -x_1, 4.0e-2 / y2);
            goo();
            return ;
        } 
""", "main,:,function,void,(,),{,foo,(,20,+,-,x_1,,,4.0e-2,/,y2,),;,goo,(,),;,return,;,},<EOF>",101))
    def test_program_12(self):
        self.assertTrue(TestLexer.test("""
            main: function void () {
                a = 2 + 2%2/2*-2 ;
                b = 1*1--1+1/1 ;
                c = a + b / (2*1.0+1) ;                
            }
""", "main,:,function,void,(,),{,a,=,2,+,2,%,2,/,2,*,-,2,;,b,=,1,*,1,-,-,1,+,1,/,1,;,c,=,a,+,b,/,(,2,*,1.0,+,1,),;,},<EOF>",101))
    def test_program_13(self):
        self.assertTrue(TestLexer.test("""
            main: function void () {
                a = true ;
                b = !a && false || (false && true || true) ;  
                c = !!b || false ;             
            }
""", "main,:,function,void,(,),{,a,=,true,;,b,=,!,a,&&,false,||,(,false,&&,true,||,true,),;,c,=,!,!,b,||,false,;,},<EOF>",101))
    def test_program_14(self):
        self.assertTrue(TestLexer.test("""
            True : string = "It's true!" 
            false : string = "it's not true..." 
""", "True,:,string,=,It's true!,false,:,string,=,it's not true...,<EOF>",101))
    def test_integer3(self):
        self.assertTrue(TestLexer.test("123 _123 1_23 0123__45_6 __123", "123,_123,123,0,123456,__123,<EOF>", 1002))
    def test_integer5(self):
        self.assertTrue(TestLexer.test("1_23__456_", "123456,_,<EOF>", 1003))
    
    
    
    def test_unclosed_string19(self):
        self.assertTrue(TestLexer.test(""""\\"Open string""", """Unclosed String: \\"Open string""", 1012))
    
    
    def test_unclosed_string18(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\n"|"|b6783\\")&* ""","""Unclosed String: %^&*(""",1018))
      
    """test identifiers"""
    def test_identifier_1(self):
        self.assertTrue(TestLexer.test(	" abcd","abcd,<EOF>",101))
    def test_identifier_2(self):
        self.assertTrue(TestLexer.test(	"AbCd","AbCd,<EOF>",102))
    def test_identifier_3(self):
        self.assertTrue(TestLexer.test(	"abc1","abc1,<EOF>",103))
    def test_identifier_4(self):
        self.assertTrue(TestLexer.test(	"_etg","_etg,<EOF>",104))
    def test_identifier_5(self):
        self.assertTrue(TestLexer.test(	"_bcd1234","_bcd1234,<EOF>",105))
    def test_identifier_6(self):
        self.assertTrue(TestLexer.test(	"a_","a_,<EOF>",106))
    def test_identifier_7(self):
        self.assertTrue(TestLexer.test(	"mg_311_acjav","mg_311_acjav,<EOF>",107))
        
    """test integer"""
    def test_integer_8(self):
        self.assertTrue(TestLexer.test(	"0 1_3 24_5 333_1","0,13,245,3331,<EOF>",108))
    def test_integer_9(self):
        self.assertTrue(TestLexer.test(	"0 6_3 83_5 3_2_3_1","0,63,835,3231,<EOF>",109))
    def test_integer_10(self):
        self.assertTrue(TestLexer.test(	"123asd","123,asd,<EOF>",110))
    def test_integer_11(self):
        self.assertTrue(TestLexer.test(	"10_2_3_4","10234,<EOF>",111))
    def test_integer_12(self):
        self.assertTrue(TestLexer.test(	"0abc","0,abc,<EOF>",112))
        
    """test float"""
    def test_float_13(self):
        self.assertTrue(TestLexer.test(	"e1 1e11 5E-3 2E-10","e1,1e11,5E-3,2E-10,<EOF>",113))
    def test_float_14(self):
        self.assertTrue(TestLexer.test(	"1.2e3","1.2e3,<EOF>",114))
    def test_float_15(self):
        self.assertTrue(TestLexer.test(	"7E-10","7E-10,<EOF>",115))
    def test_float_16(self):
        self.assertTrue(TestLexer.test(	"1_234.567","1234.567,<EOF>",116))
    def test_float_17(self):
        self.assertTrue(TestLexer.test(	"1_234.567abc","1234.567,abc,<EOF>",117))
    def test_float_18(self):
        self.assertTrue(TestLexer.test(	"1e-5","1e-5,<EOF>",118))
        # ok
    """test boolean"""
    def test_boolean_19(self):
        self.assertTrue(TestLexer.test(	"true","true,<EOF>",119))
    def test_boolean_20(self):
        self.assertTrue(TestLexer.test(	"false true","false,true,<EOF>",120))
    def test_boolean_21(self):
        self.assertTrue(TestLexer.test(	"false","false,<EOF>",121))
    def test_boolean_22(self):
        self.assertTrue(TestLexer.test(	"true true","true,true,<EOF>",122))
    def test_boolean_23(self):
        self.assertTrue(TestLexer.test(	"false false","false,false,<EOF>",123))
    
    """test string"""
    def test_string_24(self):
        self.assertTrue(TestLexer.test(	
            r""""String contain tab \t"
            """,
            """String contain tab \\t,<EOF>""",124))
    # def test_string_25(self):
        self.assertTrue(TestLexer.test(r""" "You said: abc?""",
            "Unclosed String: You said: abc?",125))
    def test_string_26(self):
        self.assertTrue(TestLexer.test("""  "abc"  ""","abc,<EOF>",126))
    def test_string_27(self):
        self.assertTrue(TestLexer.test(""" "abcasc" ""","abcasc,<EOF>",127))
    def test_string_28(self):
        self.assertTrue(TestLexer.test(r""" "abc\\a" """,r"""abc\\a,<EOF>""",128))
    def test_string_29(self):
        self.assertTrue(TestLexer.test(r""" "abc\t" """,r"""abc\t,<EOF>""",129))
    # def test_string_30(self):
        self.assertTrue(TestLexer.test(r""" "abc\a" """,r"""Illegal Escape In String: abc\a""",130))
    def test_string_31(self):
        self.assertTrue(TestLexer.test(r""" "abc\\" """,r"""abc\\,<EOF>""",131))
    def test_string_32(self):
        self.assertTrue(TestLexer.test(r""" "ab\"hvc" """,r"""ab\"hvc,<EOF>""",132))
    def test_string_33(self):
        self.assertTrue(TestLexer.test(r""" "ab\?" """,r"""Illegal Escape In String: ab\?""",133))
    def test_string_34(self):
        self.assertTrue(TestLexer.test(r""" "abc\" """,r"""Unclosed String: abc\" """,134))
    def test_string_35(self):
        self.assertTrue(TestLexer.test(r""" "asd\a" """, r"""Illegal Escape In String: asd\a""" ,135))
    def test_string_36(self):
        self.assertTrue(TestLexer.test(r""" "asd123asd\t123" """, r"""asd123asd\t123,<EOF>""" ,136))
    def test_string_37(self):
        self.assertTrue(TestLexer.test(r""" "asdkas\\\\" """, r"""asdkas\\\\,<EOF>""" ,137))
    def test_string_38(self):
        self.assertTrue(TestLexer.test(r""" "test """, r"""Unclosed String: test """ ,138))
    def test_string_39(self):
        self.assertTrue(TestLexer.test(""" "test""test" ""","""test,test,<EOF>""" ,139))
    def test_string_40(self):
        self.assertTrue(TestLexer.test(""" "a b c d e" """, """a b c d e,<EOF>""" ,140))
    def test_string_41(self):
        self.assertTrue(TestLexer.test(r""" "a b c \t" """, r"""a b c \t,<EOF>""" ,141))
    def test_string_42(self):
        self.assertTrue(TestLexer.test(r""" "a b c \a" """, r"""Illegal Escape In String: a b c \a""" ,142))
    def test_string_43(self):
        self.assertTrue(TestLexer.test(r""" "abc \" \" " """, r"""abc \" \" ,<EOF>""" ,143))
    def test_string_44(self):
        self.assertTrue(TestLexer.test(r""" "\"\\\\" """, r"""\"\\\\,<EOF>""" ,144))
    def test_string_45(self):
        self.assertTrue(TestLexer.test(r""" "\\\\\"\a\t" """, r"""Illegal Escape In String: \\\\\"\a""" ,145))
    
    """ Test Specific Characters """
    def test_characters_46(self):
        self.assertTrue(TestLexer.test(
            r"""+ - * / %
                ! && || == =
                != < <= > >=
                . ::
                ( ) [ ] .. , ; : { }
            """,
            "+,-,*,/,%,!,&&,||,==,=,!=,<,<=,>,>=,.,::,(,),[,],.,.,,,;,:,{,},<EOF>",
            146
        ))
        
    """ Test Comment """
    def test_comment_47(self):
        self.assertTrue(TestLexer.test(r""" /* comment */ ""","<EOF>",147))
    def test_comment_48(self):
        self.assertTrue(TestLexer.test(r""" /* comment \n */ ""","<EOF>", 148))
    def test_comment_49(self):
        self.assertTrue(TestLexer.test(r""" /* comment without close ""","/,*,comment,without,close,<EOF>", 149))
    def test_comment_50(self):
        self.assertTrue(TestLexer.test(r""" // This is a comment ""","<EOF>", 150))
    def test_comment_51(self):
        self.assertTrue(TestLexer.test(r""" /* This is a comment \n
                                       This is line 2 of comment \n
                                       This is line 3 of comment */""","<EOF>", 151))
    
    """ Test Invalid Identifiers """
    def test_invalid_52(self):
        self.assertTrue(TestLexer.test(
            r"""123abc 123_abc 0123_123abc""","123,abc,123,_abc,0,123123,abc,<EOF>",152 ))
    def test_invalid_53(self):
        self.assertTrue(TestLexer.test(
            r"""_12371 __12___""","_12371,__12___,<EOF>",153 ))
    def test_invalid_54(self):
        self.assertTrue(TestLexer.test(
            r"""1e111021301 0eE10111""","1e111021301,0,eE10111,<EOF>",154))
        # ok
    def test_55(self):
        self.assertTrue(TestLexer.test(r""" "\"abc\\\\abc" """, r"""\"abc\\\\abc,<EOF>""" ,155))
    def test_56(self):
        self.assertTrue(TestLexer.test(r""" "xya ` afv" """, r"""xya ` afv,<EOF>""" ,156))
    def test_57(self):
        self.assertTrue(TestLexer.test(r""" "abc\t\r\f\n" """, r"""abc\t\r\f\n,<EOF>""" ,157))
    def test_58(self):
        self.assertTrue(TestLexer.test(r""" "asd\\\\\"" """, r"""asd\\\\\",<EOF>""" ,158))
    def test_59(self):
        self.assertTrue(TestLexer.test(r""" 1238970b123 """, r"""1238970,b123,<EOF>""" ,159))
    def test_60(self):
        self.assertTrue(TestLexer.test(""" "abc""abc" ""","""abc,abc,<EOF>""" ,160))
        
    """ Test Error Token """
    def test_err_tok_61(self):
        self.assertTrue(TestLexer.test(
            r"""
            & ^ % $ # ... \
                ""","Error Token &",161  ))
    def test_err_tok_62(self):
        self.assertTrue(TestLexer.test(
            r"""
            If a | b Else
            ""","If,a,Error Token |",162))
    def test_err_tok_63(self):
        self.assertTrue(TestLexer.test(
            r"""
            abc = abc & 2
            ""","abc,=,abc,Error Token &",163))
    def test_identifier_64(self):
        self.assertTrue(TestLexer.test(
            r"""
            xyz
            a = 5
            ""","xyz,a,=,5,<EOF>",164))
    def test_identifier_65(self):
        self.assertTrue(TestLexer.test(
            r"""
            integer ab2, ab3, ac
            ""","integer,ab2,,,ab3,,,ac,<EOF>",165))
        
    """ Test Valid Keywords """
    def test_keywords_66(self):
        self.assertTrue(TestLexer.test(
            r"""auto break boolean do else false float for function if integer return string true while void out continue of inherit array
            """,
            r"""auto,break,boolean,do,else,false,float,for,function,if,integer,return,string,true,while,void,out,continue,of,inherit,array,<EOF>""",
            166))
        
    """test float literal"""
    def test_float_67(self):
        self.assertTrue(TestLexer.test(	"1.123","1.123,<EOF>",167))
    def test_float_68(self):
        self.assertTrue(TestLexer.test(	"0.123","0.123,<EOF>",168))
    def test_float_69(self):
        self.assertTrue(TestLexer.test(	"00.123","0,0.123,<EOF>",169))
    def test_float_70(self):
        self.assertTrue(TestLexer.test(	"123.2e3","123.2e3,<EOF>",170))
    def test_float_71(self):
        self.assertTrue(TestLexer.test(	"1_3_2.2e-33","132.2e-33,<EOF>",171))
    def test_float_72(self):
        self.assertTrue(TestLexer.test(	"0.123E-10","0.123E-10,<EOF>",172))
    def test_float_73(self):
        self.assertTrue(TestLexer.test(	"12_3_4.123_3_4","1234.123,_3_4,<EOF>",173))
    def test_float_74(self):
        self.assertTrue(TestLexer.test(	"00.001","0,0.001,<EOF>",174))
    # ok
    """test mixed"""
    def test_comment_75(self):
        self.assertTrue(TestLexer.test(r""" // This is a comment \n
                                       This is a comment""","This,is,a,comment,<EOF>", 175))
    def test_mixed_76(self):
        self.assertTrue(TestLexer.test(
            r"""
            "bac abc and \t \r \\a\\b\b\n\\t\\\\\r ppl !!!"
            """,
            r"""bac abc and \t \r \\a\\b\b\n\\t\\\\\r ppl !!!,<EOF>""",176))
    def test_mixed_77(self):
        self.assertTrue(TestLexer.test(
            r"""
            "bac abc and \t \r \\a\\b\b\n\\t\\\\\r kdf"
            """,
            r"""bac abc and \t \r \\a\\b\b\n\\t\\\\\r kdf,<EOF>""",177))
    def test_mixed_78(self):
        self.assertTrue(TestLexer.test(r""" "abc" "deg "=-132=42=12-"hasagi """,
                                       "abc,deg ,=,-,132,=,42,=,12,-,Unclosed String: hasagi ", 178))
    def test_mixed_79(self):
        self.assertTrue(TestLexer.test(r""" "YASUO \c\d\e" """, r"Illegal Escape In String: YASUO \c", 179))
    def test_mixed_80(self):
        self.assertTrue(TestLexer.test(r""" "ZED d\hef" """, r"Illegal Escape In String: ZED d\h", 180))
    def test_mixed_81(self):
        self.assertTrue(TestLexer.test(r""" "test""asd """, r"""test,Unclosed String: asd """  ,181))
    # ok
    # def test_mixed_82(self):
        self.assertTrue(TestLexer.test(r"""a = Array[Int,0]""", r"""a,=,Array,[,Int,,,0,],<EOF>""" ,182))
    def test_mixed_83(self):
        self.assertTrue(TestLexer.test(r"""Var a : Int; " """, r"""Var,a,:,Int,;,Unclosed String:  """ ,183))
    def test_mixed_84(self):
        self.assertTrue(TestLexer.test(r"""a = "mystring" """, r"""a,=,mystring,<EOF>""" ,184))
    def test_mixed_85(self):
        self.assertTrue(TestLexer.test(r"""a = "my string" """, r"""a,=,my string,<EOF>""" ,185))
    def test_mixed_86(self):
        self.assertTrue(TestLexer.test(r""" "123_1230b01""", r"""Unclosed String: 123_1230b01""" ,186))
    def test_mixed_87(self):
        self.assertTrue(TestLexer.test(r"""// A C++ style comment""", r"""<EOF>""" ,187))
    def test_mixed_88(self):
        self.assertTrue(TestLexer.test(r"""/* A C-style comment */""", r"""<EOF>""" ,188))
    def test_mixed_89(self):
        self.assertTrue(TestLexer.test(r"""a = "mystring \t" """, r"""a,=,mystring \t,<EOF>""" ,189))
    def test_mixed_90(self):
        self.assertTrue(TestLexer.test(r"""a = "mystring\\\\" """, r"""a,=,mystring\\\\,<EOF>""" ,190))
    def test_mixed_91(self):
        self.assertTrue(TestLexer.test(r""" "asdf ` asdf" """, r"""asdf ` asdf,<EOF>""" ,191))
    def test_mixed_92(self):
        self.assertTrue(TestLexer.test(r""" "asdf\t\r\f" """, r"""asdf\t\r\f,<EOF>""" ,192))
    def test_mixed_93(self):
        self.assertTrue(TestLexer.test(r""" "asd\\\\\"" """, r"""asd\\\\\",<EOF>""" ,193))
    def test_mixed_94(self):
        self.assertTrue(TestLexer.test(r""" 1238970b123 """, r"""1238970,b123,<EOF>""" ,194))
    def test_mixed_95(self):
        self.assertTrue(TestLexer.test(r""" 123"asasd \t \f \a" """, r"""123,Illegal Escape In String: asasd \t \f \a""" ,195))
    def test_mixed_96(self):
        self.assertTrue(TestLexer.test(r"""101023456"123"" """, r"""101023456,123,Unclosed String:  """ ,196))
    def test_mixed_97(self):
        self.assertTrue(TestLexer.test(r"""aAaAbBbB09809""", r"""aAaAbBbB09809,<EOF>""" ,197))
    def test_mixed_98(self):
        self.assertTrue(TestLexer.test(r"""098098_123123aBaBb""", r"""0,98098123123,aBaBb,<EOF>""" ,198))
    def test_mixed_99(self):
        self.assertTrue(TestLexer.test(r""" 1010101010 """, r"""1010101010,<EOF>""" ,199))
    def test_mixed_200(self):
        self.assertTrue(TestLexer.test(r""" 0.123E-10AFC """, r"""0.123E-10,AFC,<EOF>""" ,200))
    
    

    
    
    
 

 
 
 
    
 