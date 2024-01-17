import unittest
from TestUtils import TestLexer


class LexerSuite(unittest.TestCase):
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
        # ok
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
        #ok
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
    #ok
    """test string"""
    def test_string_24(self):
        self.assertTrue(TestLexer.test(	
            r""""String contain tab \t"
            """,
            """String contain tab \\t,<EOF>""",124))
    def test_string_25(self):
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
    def test_string_30(self):
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
    # ok
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
    # ok
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
        # ok
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
        # ok
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
    def test_mixed_82(self):
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
        
        
    # ok pass hết