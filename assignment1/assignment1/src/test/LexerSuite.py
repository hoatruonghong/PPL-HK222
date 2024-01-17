import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):
    def test_inline_comment(self):
        self.assertTrue(TestLexer.test("// This is a comment", "<EOF>", 101))
    def test_inline_comment2(self):
        self.assertTrue(TestLexer.test("// This is a comment \n", "<EOF>", 102))
    def test_inline_comment3(self):
        self.assertTrue(TestLexer.test("// This is a comment with \"\\\" inside.", "<EOF>", 103))
    def test_inline_comment4(self):
        self.assertTrue(TestLexer.test("//*This is still a inline comment", "<EOF>", 104))
    def test_inline_comment5(self):
        self.assertTrue(TestLexer.test("//*This is still a inline comment*/", "<EOF>", 105))
        
    def test_block_comment1(self):
        self.assertTrue(TestLexer.test("/* This is a block comment */", "<EOF>", 106))
    def test_block_comment2(self):
        self.assertTrue(TestLexer.test("/* This is a block comment \nwith multiple lines */", "<EOF>", 107))
    def test_block_comment3(self):
        self.assertTrue(TestLexer.test("/* This is a block //comment */", "<EOF>", 108))
    def test_block_comment4(self):
        self.assertTrue(TestLexer.test("/* This is a block comment end with \"* /\" */", "<EOF>", 109))
    def test_block_comment5(self):
        self.assertTrue(TestLexer.test("/* This is a block comment \n//Inline Comment */", "<EOF>", 110))
    def test_block_comment6(self):
        self.assertTrue(TestLexer.test("/* This is a unclose block comment ", "/,*,This,is,a,unclose,block,comment,<EOF>", 111))
    def test_block_comment7(self):
        self.assertTrue(TestLexer.test("/* This is another block comment */ */", "*,/,<EOF>", 112))
        
    def test_nested_comment1(self):
        self.assertTrue(TestLexer.test("// A line comment // contains another line comment . ", "<EOF>", 113))
    def test_nested_comment2(self):
        self.assertTrue(TestLexer.test("/*a block cmt /*cover a block cmt*/ */ ", "*,/,<EOF>", 114))
    def test_nested_comment3(self):
        self.assertTrue(TestLexer.test("/*block comment 1*/\n/*block comment2*///inline comment", "<EOF>", 115))
    
    def test_identifier(self):
        self.assertTrue(TestLexer.test("my name is Hoa", "my,name,is,Hoa,<EOF>", 116))
    def test_identifier2(self):
        self.assertTrue(TestLexer.test("__", "__,<EOF>", 117))
    def test_identifier3(self):
        self.assertTrue(TestLexer.test("Ident 1 id1", "Ident,1,id1,<EOF>", 118))
    def test_identifier4(self):
        self.assertTrue(TestLexer.test("X/123", "X,/,123,<EOF>", 119))
    def test_identifier5(self):
        self.assertTrue(TestLexer.test("_count 123number||sum", "_count,123,number,||,sum,<EOF>", 120))
    def test_identifier6(self):
        self.assertTrue(TestLexer.test("1day, I go to _school123_.;", "1,day,,,I,go,to,_school123_,.,;,<EOF>", 121))
    def test_identifier7(self):
        self.assertTrue(TestLexer.test("1Cat+2_Dogs", "1,Cat,+,2,_Dogs,<EOF>", 122))
    
    def test_keyword1(self):
        self.assertTrue(TestLexer.test("autobreakboolean", "autobreakboolean,<EOF>", 123))
    def test_keyword2(self):
        self.assertTrue(TestLexer.test("integer function void", "integer,function,void,<EOF>", 124))
        
    def test_integer1(self):
        self.assertTrue(TestLexer.test("0090", "0,0,90,<EOF>", 125))
    def test_integer2(self):
        self.assertTrue(TestLexer.test("-090x90", "-,0,90,x90,<EOF>", 126))
    def test_integer3(self):
        self.assertTrue(TestLexer.test("0_123 123 _123 1_23 123_ __123", "0,_123,123,_123,123,123,_,__123,<EOF>", 127))
    def test_integer4(self):
        self.assertTrue(TestLexer.test("123*901/10", "123,*,901,/,10,<EOF>", 128))
    def test_integer5(self):
        self.assertTrue(TestLexer.test("1_234__567  1__23_4_", "1234,__567,1,__23_4_,<EOF>", 129))
    def test_integer6(self):
        self.assertTrue(TestLexer.test("5 + 100/20", "5,+,100,/,20,<EOF>", 130))
    def test_integer7(self):
        self.assertTrue(TestLexer.test("-1000-10+-100/1", "-,1000,-,10,+,-,100,/,1,<EOF>", 131))
    def test_integer8(self):
        self.assertTrue(TestLexer.test("80 < 120 && (3-7) >= 7", "80,<,120,&&,(,3,-,7,),>=,7,<EOF>", 132))
    def test_integer9(self):
        self.assertTrue(TestLexer.test("5!=8 || 12%4 == 0", "5,!=,8,||,12,%,4,==,0,<EOF>", 133))
    def test_integer10(self):
        self.assertTrue(TestLexer.test("x00_0 010 1000x", "x00_0,0,10,1000,x,<EOF>", 134))
    
    def test_float0(self):
        self.assertTrue(TestLexer.test("e-10 0E e+0e 00.e .e-10 .0e1 .0e-1","e,-,10,0,E,e,+,0,e,0,0,.,e,.,e,-,10,.0e1,.0e-1,<EOF>",135))       
    def test_float1(self):
        self.assertTrue(TestLexer.test("1.2e10", "1.2e10,<EOF>", 136))
    def test_float2(self):
        self.assertTrue(TestLexer.test(" 7.5 0.6 ", "7.5,0.6,<EOF>", 137))
    def test_float3(self):
        self.assertTrue(TestLexer.test(" 5.1+1e5 ","5.1,+,1e5,<EOF>",138))
    def test_float4(self):
        self.assertTrue(TestLexer.test(" 6.8+9.2 ","6.8,+,9.2,<EOF>",139))
    def test_float5(self):
        self.assertTrue(TestLexer.test(" -1.3+1e3 ","-,1.3,+,1e3,<EOF>",140))
    def test_float6(self):
        self.assertTrue(TestLexer.test("1. .6  ","1,.,.,6,<EOF>",141))
    def test_float7(self):
        self.assertTrue(TestLexer.test(" 7E15 ","7E15,<EOF>",142))
    def test_float8(self):
        self.assertTrue(TestLexer.test(" 1.0e ","1.0,e,<EOF>",143))
    def test_float9(self):
        self.assertTrue(TestLexer.test("4.1e3 ","4.1e3,<EOF>",144))
    def test_float10(self):
        self.assertTrue(TestLexer.test(" 5e-8+6 ","5e-8,+,6,<EOF>",145))
    def test_float11(self):
        self.assertTrue(TestLexer.test(" 10.0e-2.2e-3 ","10.0e-2,.2e-3,<EOF>",146))
    def test_float12(self):
        self.assertTrue(TestLexer.test(" 1_23.1e-1 ","123.1e-1,<EOF>",147))
    
    def test_string1(self):
        self.assertTrue(TestLexer.test(""""Hello World !" ""","""Hello World !,<EOF>""",148))
    def test_string2(self):
        self.assertTrue(TestLexer.test(""""1 Cat + 2 Dogs ::::: 12 Birds, 3 Spiders in the picture." ""","""1 Cat + 2 Dogs ::::: 12 Birds, 3 Spiders in the picture.,<EOF>""",149))
    def test_string3(self):
        self.assertTrue(TestLexer.test(""""Hello World !\"\n\"The result is: \"2 ""","""Hello World !,The result is: ,2,<EOF>""",150))
    def test_string4(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\t"|"|b6783\\")&* ""","""%^&*(	,Error Token |""",151))
    
    def test_string_comment1(self):
        self.assertTrue(TestLexer.test(""" "Hello /*My*/ World" ""","""Hello /*My*/ World,<EOF>""",152))
    def test_string_comment2(self):
        self.assertTrue(TestLexer.test(""" "Hello World/* " */  ""","""Hello World/* ,*,/,<EOF>""",153))
    def test_string_comment3(self):
        self.assertTrue(TestLexer.test(""" "Hello //My World" ""","""Hello //My World,<EOF>""",154))
    
    def test_string_escape(self):
        self.assertTrue(TestLexer.test(""" "This is a string containing tab \t." """, """This is a string containing tab \t.,<EOF>""", 155))
    def test_string_escape2(self):
        self.assertTrue(TestLexer.test(""" "He asked me: \"Where is John?\"" """, """He asked me: \"Where is John?\",<EOF>""", 156))
    def test_string_escape3(self):
        self.assertTrue(TestLexer.test(""" "This sentence contains new line\n." """, """Unclosed String: This sentence contains new line""", 157))
    def test_string_escape4(self):
        self.assertTrue(TestLexer.test(""" "Print it ( a line char \\n )" """, """Print it ( a line char \\n ),<EOF>""", 158))
    def test_string_escape5(self):
        self.assertTrue(TestLexer.test(""" "There is a backspace \b. before here." """, """There is a backspace \b. before here.,<EOF>""", 159))
    def test_string_escape6(self):
        self.assertTrue(TestLexer.test(""" "Multiple chars \\\\" """, """Multiple chars \\\\,<EOF>""", 160))
    def test_string_escape7(self):
        self.assertTrue(TestLexer.test(""" "He asked me: \\"Where is John?\\"" ""","""He asked me: \"Where is John?\",<EOF>""", 161))
    def test_string_escape8(self):
        self.assertTrue(TestLexer.test("""" Print integer number by \"printInt(anArg: int)\"" """, """ Print integer number by ,printInt,(,anArg,:,int,),,<EOF>""", 162))
    def test_string_escape9(self):
        self.assertTrue(TestLexer.test(""""We combine \' \'" """, """Unclosed String: We combine ' '" """, 163))
    def test_string_escape10(self):
        self.assertTrue(TestLexer.test(""""This is a string containing /*comment*/" """, """This is a string containing /*comment*/,<EOF>""", 164))
    def test_string_escape11(self):
        self.assertTrue(TestLexer.test(""""He said: \'He said:\'I saw him.\'\'" """, """He said: \'He said:\'I saw him.\'\',<EOF>""", 165))
    def test_string_escape12(self):
        self.assertTrue(TestLexer.test(""""He said: \"He said:\"I saw him.\"\"" """, """He said: \"He said:\"I saw him.\"\",<EOF>""", 166))
    def test_unclosed_string13(self):
        self.assertTrue(TestLexer.test(""" " " "" " """,""" ,,Unclosed String:  """,167))
    def test_unclosed_string14(self):
        self.assertTrue(TestLexer.test("""  "Test \n Unclosed String"  ""","""Unclosed String: Test """,168))
    def test_unclosed_string15(self):
        self.assertTrue(TestLexer.test(""" "Test Unclosed String \n" ""","""Unclosed String: Test Unclosed String """,169))
    def test_unclosed_string16(self):
        self.assertTrue(TestLexer.test(""" "line 1\\n line 2\n" ""","""Unclosed String: line 1\\n line 2""",170))
    def test_unclosed_string17(self):
        self.assertTrue(TestLexer.test(""" hi "my world \n ""","""hi,Unclosed String: my world """,171))
    def test_unclosed_string18(self):
        self.assertTrue(TestLexer.test(""" "%^&*(\n"|"|b6783\\")&* ""","""Unclosed String: %^&*(""",172))
    def test_unclosed_string19(self):
        self.assertTrue(TestLexer.test(""" "Open string """, """Unclosed String: Open string """, 173))
    def test_unclosed_string20(self):
        self.assertTrue(TestLexer.test(""" 
            "Open string \n. " 
        ""","""Unclosed String: Open string """, 174))    
    def test_illegal_string4(self):
        self.assertTrue(TestLexer.test("""  "abc123a\\mabc"  ""","""Illegal Escape In String: abc123a\\m""",175))
    def test_illegal_string5(self):
        self.assertTrue(TestLexer.test("""   123-4"abc123a\\b\\iasVm"  ""","""123,-,4,Illegal Escape In String: abc123a\\b\\i""",176))
    def test_illegal_string6(self):
        self.assertTrue(TestLexer.test("""  "Hi, this is abc \\h\\n\\t "  ""","""Illegal Escape In String: Hi, this is abc \h""",177))
    def test_illegal_string7(self):
        self.assertTrue(TestLexer.test(""" "     " " " "" "\\t\\b\\g" ""","""     , ,,Illegal Escape In String: \\t\\b\\g""",178))
    # def test_illegal_string8(self):
    #     self.assertTrue(TestLexer.test(""" "X=004*0875.E-2\\087.02" ""","""Illegal Escape In String: X=004*0875.E-2\0""",101))
    # def test_illegal_string9(self):
    #     self.assertTrue(TestLexer.test(""" "illegal_escape\" ""","""Illegal Escape In String: illegal_escape\"""",101))
    def test_illegal_string10(self):
        self.assertTrue(TestLexer.test(""" 
        "t \ {abcd}\\efg"
        ""","Illegal Escape In String: t \ ",179))
        
        
    def test_operator(self):
        self.assertTrue(TestLexer.test("+ - * / ! % || && != == <= >= > < = :::::", "+,-,*,/,!,%,||,&&,!=,==,<=,>=,>,<,=,::,::,:,<EOF>", 180))
    def test_operator2(self):
        self.assertTrue(TestLexer.test("2*2 + 2^ 1", "2,*,2,+,2,Error Token ^", 181))
    def test_operator3(self):
        self.assertTrue(TestLexer.test("do {print(a);} while (a & b);", "do,{,print,(,a,),;,},while,(,a,Error Token &", 182))
    def test_operator4(self):
        self.assertTrue(TestLexer.test("income=income + salary*1.2*rate[1]+month#3;", "income,=,income,+,salary,*,1.2,*,rate,[,1,],+,month,Error Token #", 183))
    def test_operator5(self):
        self.assertTrue(TestLexer.test("cost = sum((y-h(i))**2)", "cost,=,sum,(,(,y,-,h,(,i,),),*,*,2,),<EOF>", 184))
    def test_operator6(self):
        self.assertTrue(TestLexer.test("x = (4 + 3i)(2 + 5i).i^2", "x,=,(,4,+,3,i,),(,2,+,5,i,),.,i,Error Token ^", 185))
    def test_operator7(self):
        self.assertTrue(TestLexer.test("+-*/%*()/*//$#", "+,-,*,/,%,*,(,),/,*,<EOF>", 186))

    def test_separators(self):
        self.assertTrue(TestLexer.test("(  ) [ ] { } ; ,  =", "(,),[,],{,},;,,,=,<EOF>", 187))
    
    def test_full1(self):
        self.assertTrue(TestLexer.test("array[1+2,0]=0;","array,[,1,+,2,,,0,],=,0,;,<EOF>",188))
    def test_full2(self):
        self.assertTrue(TestLexer.test("x,y,z: float = 1.20e10, 7E-2, 3*a","x,,,y,,,z,:,float,=,1.20e10,,,7E-2,,,3,*,a,<EOF>",189))
    def test_full3(self):
        self.assertTrue(TestLexer.test("20>>3<<4<===>=b","20,>,>,3,<,<,4,<=,==,>=,b,<EOF>",190))
    def test_full4(self):
        self.assertTrue(TestLexer.test("(2.2+03)||a!==3&a","(,2.2,+,0,3,),||,a,!=,=,3,Error Token &",191))
    def test_full5(self):
        self.assertTrue(TestLexer.test("super(a[Integer,0],b*c-d,+3.4e-1+.e-2);","super,(,a,[,Integer,,,0,],,,b,*,c,-,d,,,+,3.4e-1,+,.,e,-,2,),;,<EOF>",192)) 
    
    def test_statement1(self):
        self.assertTrue(TestLexer.test("printInteger(123);","printInteger,(,123,),;,<EOF>", 193)) 
    def test_statement2(self):
        self.assertTrue(TestLexer.test("arr: array[1,2] of integer = {{-1,2}};","arr,:,array,[,1,,,2,],of,integer,=,{,{,-,1,,,2,},},;,<EOF>", 194)) 
    def test_statement3(self):
        self.assertTrue(TestLexer.test("printInteger(123);","printInteger,(,123,),;,<EOF>", 195)) 
    def test_statement4(self):
        self.assertTrue(TestLexer.test("a : integer = ?","a,:,integer,=,Error Token ?", 196)) 

    def test_program_1(self):
        self.assertTrue(TestLexer.test("""
main : function void() {                                      
    printString("Hello World");
    return ;
}
""", "main,:,function,void,(,),{,printString,(,Hello World,),;,return,;,},<EOF>",197))
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
}}""", "main,:,function,void,(,),{,{,{,{,},},},},<EOF>",198))
    def test_program_3(self):
        self.assertTrue(TestLexer.test("""
a : integer = 0;
main : function void() {                                      
    return a;
}
""", "a,:,integer,=,0,;,main,:,function,void,(,),{,return,a,;,},<EOF>",199))
    def test_program_4(self):
        self.assertTrue(TestLexer.test("""
a : integer = 0;
main : function void() {                                      
    return a;
}
""", "a,:,integer,=,0,;,main,:,function,void,(,),{,return,a,;,},<EOF>",200))
        ## 100 testcases done

#     def test_program_5(self):
#         self.assertTrue(TestLexer.test("""
# {
# r, s: integer;
# r = 2.0;
# a, b: array [5] of integer;
# s = r * r * myPI;
# a[0] = s;
# }
# """, "{,r,,,s,:,integer,;,r,=,2.0,;,a,,,b,:,array,[,5,],of,integer,;,s,=,r,*,r,*,myPI,;,a,[,0,],=,s,;,},<EOF>",1000))
        
#     def test_program_6(self):
#         self.assertTrue(TestLexer.test("""
# main: function void () {
#     if (a>b) if (true) printString("TRUE"); else printString("FALSE");
#     else printInteger(b);
#     return;
# }
# """, "main,:,function,void,(,),{,if,(,a,>,b,),if,(,true,),printString,(,TRUE,),;,else,printString,(,FALSE,),;,else,printInteger,(,b,),;,return,;,},<EOF>",1001))
#     def test_program_7(self):
#         self.assertTrue(TestLexer.test("""
# main: function void () {
#     for (i = n, , i%2) printString("Computer is working...\n");
# }
# """, "main,:,function,void,(,),{,for,(,i,=,n,,,,,i,%,2,),printString,(,Unclosed String: Computer is working...\n",1002))
#     def test_program_8(self):
#         self.assertTrue(TestLexer.test("""
#             main: function void () {
#                 do {
#                     if (a == 10) break;
#                     a = a - 1; 
#                     printInteger(a);
#                 }
#                 while(a > 0);
#             }
# """, "main,:,function,void,(,),{,do,{,if,(,a,==,10,),break,;,a,=,a,-,1,;,printInteger,(,a,),;,},while,(,a,>,0,),;,},<EOF>",1003))
#     def test_program_9(self):
#         self.assertTrue(TestLexer.test("""
#             main : function void() {
#                 a, b : integer = round(123.0e2), randomInt();
#                 /*
#                 Calculate sum of 2 numbers a & b
#                 */
#                 sum : integer = a + b + arr[0,0];
#                 print(a, sum);
#                 return ;
#             }
# """, "main,:,function,void,(,),{,a,,,b,:,integer,=,round,(,123.0e2,),,,randomInt,(,),;,sum,:,integer,=,a,+,b,+,arr,[,0,,,0,],;,print,(,a,,,sum,),;,return,;,},<EOF>",1004))
#     def test_program_10(self):
#         self.assertTrue(TestLexer.test("""
#             main: function void() {
#                 a : string = "Hello world"; // string 
#                 return a::"!";
#             }  
# """, "main,:,function,void,(,),{,a,:,string,=,Hello world,;,return,a,::,!,;,},<EOF>",1005))
#     def test_program_11(self):
#         self.assertTrue(TestLexer.test("""
#             main : function void() {
#             foo(2__0 + -x_1, 4.0e-2 / y2);
#             goo();
#             return ;
#         } 
# """, "main,:,function,void,(,),{,foo,(,2,__0,+,-,x_1,,,4.0e-2,/,y2,),;,goo,(,),;,return,;,},<EOF>",1006))
#     def test_program_12(self):
#         self.assertTrue(TestLexer.test("""
#             main: function void () {
#                 a = 2 + 2%2/2*-2 ;
#                 b = 1*1--1+1/1 ;
#                 c = a + b / (2*1.0+1) ;                
#             }
# """, "main,:,function,void,(,),{,a,=,2,+,2,%,2,/,2,*,-,2,;,b,=,1,*,1,-,-,1,+,1,/,1,;,c,=,a,+,b,/,(,2,*,1.0,+,1,),;,},<EOF>",1007))
#     def test_program_13(self):
#         self.assertTrue(TestLexer.test("""
#             main: function void () {
#                 a = true ;
#                 b = !a && false || (false && true || true) ;  
#                 c = !!b || false ;             
#             }
# """, "main,:,function,void,(,),{,a,=,true,;,b,=,!,a,&&,false,||,(,false,&&,true,||,true,),;,c,=,!,!,b,||,false,;,},<EOF>",1008))
#     def test_program_14(self):
#         self.assertTrue(TestLexer.test("""
#             True : string = "It's true!" 
#             false : string = "it's not true..." 
# """, "True,:,string,=,It's true!,false,:,string,=,it's not true...,<EOF>",1009))
    
#     def test_float14(self):
#         self.assertTrue(TestLexer.test(" .2e-3 .E2 .e-22 10.0e-2.2e-3 1. 1.e2 1.2E+10 2.45e-333 0.22 0.e2 23e8 4E 9e-10.34 ",".2e-3,.,E2,.,e,-,22,10.0e-2,.2e-3,1,.,1,.,e2,1.2E+10,2.45e-333,0.22,0,.,e2,23e8,4,E,9e-10,.,34,<EOF>",1009))
    