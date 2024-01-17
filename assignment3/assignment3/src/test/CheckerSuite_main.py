import unittest
from TestUtils import TestChecker
from AST import *
from StaticError import *


class CheckerSuite(unittest.TestCase):

	def test_no_entry1(self):

		inp=r"""
		a: integer;
		b: function integer (x: integer) {
			return x;
		}
		c: boolean;
		"""

		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(inp, expect, 400))

	def test_no_entry2(self):

		inp=r"""
		a: integer;
		c: boolean;
		"""
		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(inp, expect, 401))

	def test_undeclared_1(self):

		input = r"""
		a1: integer = 5;
		b: function integer (x: integer) {
			c: integer;
			x = 1;
			return a;
		}
				main: function void () {}
		"""

		expect = str(Undeclared(Identifier(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 401))

	def test_undeclared_2(self):

		input = r"""
		a: integer = 5;
		b: function integer (x: integer) {
			x = a;
			return c;
		}
				main: function void () {}
		"""
		expect = str(Undeclared(Identifier(), "c"))

		self.assertTrue(TestChecker.test(input, expect, 402))

	def test_undeclared_3(self):

		input = r"""
		a1: integer = 5;
		b: function integer (x: integer) {
			x = 1;
			{
				c: integer = 5;
				{
					return a;
				}
			}
		}
				main: function void () {}
		"""

		expect = str(Undeclared(Identifier(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 403))

	def test_undeclared_4(self):

		input = r"""
		a: integer = 5;
		b: function integer (x: integer) {
			return c(x);
		}
				main: function void () {}
		"""

		expect = str(Undeclared(Function(), "c"))

		self.assertTrue(TestChecker.test(input, expect, 402))

	def test_undeclared_5(self):

		input = r"""
		c: function integer (d: boolean) {
			return 9;
		}
		a: integer = 5;
		b: function integer (x: integer) {
			return c(d);
		}
				main: function void () {}
		"""
		expect = str(Undeclared(Identifier(), "d"))

		self.assertTrue(TestChecker.test(input, expect, 402))

	def test_undeclared_6(self):

		input = r"""
		c: function integer (d: boolean, e: integer) {
			return 3;
		}
		a: integer = 5;
		b: function integer (x: integer) {
			return c(true, e);
		}
				main: function void () {}
		"""

		expect = str(Undeclared(Identifier(), "e"))

		self.assertTrue(TestChecker.test(input, expect, 405))

	def test_return2(self):

		input = r"""
		d: boolean = true;
		c: function boolean (d: boolean) {
			return d;
		}
		a: integer = 5;
		b: function integer (x: integer) {
			return c(d);
		}
				main: function void () {}
		"""

		expect = str(TypeMismatchInStatement(ReturnStmt(FuncCall("c", [Id("d")]))))

		self.assertTrue(TestChecker.test(input, expect, 495))

	def test_return3(self):

		input = r"""
		d: boolean = true;
		c: function auto (d: boolean) {
			return d;
		}
		a: boolean = true;
		b: function boolean (x: integer) {
			return c(a);
		}
		//		main: function void () {}
		"""

		expect = str(
			NoEntryPoint()
		)

		# self.assertTrue(TestChecker.test(input, expect, 491))
	
	def test_return4(self):
		
		input = r"""
		a: integer = 1;
		c: function auto (d: float) {
			return d;
		}
	
		main: function void () {
			a = 1 + c(1.0);
		}
		"""

		expect = str(
			TypeMismatchInStatement(AssignStmt(Id("a"), BinExpr("+", IntegerLit(1), FuncCall("c", [FloatLit(1.0)]))))
		)

		self.assertTrue(TestChecker.test(input, expect, 490))

	def test_return5(self):
		
		input = r"""
		a: array [2] of integer;
		c: function auto (d: float) {
			return d;
		}
	
		main: function void () {
			a[0] = 1 + c(1.0);
		}
		"""

		expect = str(
			TypeMismatchInStatement(AssignStmt(ArrayCell("a", [IntegerLit(0)]), BinExpr("+", IntegerLit(1), FuncCall("c", [FloatLit(1.0)]))))
		)

		self.assertTrue(TestChecker.test(input, expect, 498))

	def test_auto_func1(self):

		input = r"""
		foo : function auto ( a : integer , b : integer ) {}
		a : float = foo (1 , 2 ) ;
		b : integer = foo (1 , 2) + 1;
		main: function void () { foo(1, 2); }
  		"""
		expect = str(
			TypeMismatchInVarDecl(VarDecl("b", IntegerType(), BinExpr("+", FuncCall("foo", [IntegerLit(1), IntegerLit(2)]), IntegerLit(1))))
		)

		self.assertTrue(TestChecker.test(input, expect, 479))
		# TODO edge cases

	def test_auto_func2(self):
		
		input = r"""
		foo : function auto ( a : integer , b : integer ) {}
		b : integer = foo (1 , 2) + 1;
		a : float = foo (1 , 2 ) ;
  		"""
		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 492))



	def test_redeclared_1(self):

		input = r"""
		a: integer = 5;
		b: integer = 6;
		a: integer = 6;
				main: function void () {}
		"""

		expect = str(Redeclared(Variable(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 404))

	def test_redeclared_2(self):

		input = r"""
		fn: function integer (x: integer) {
			return x;
			}
			fn: function integer (x: integer) {
				return x;
				}
		main: function void () {}
		"""

		expect = str(Redeclared(Function(), "fn"))

		self.assertTrue(TestChecker.test(input, expect, 405))

	def test_redeclared_3(self):

		input = r"""
		fn: function void (x: integer) {
			x: integer = 5;
			return;
		}
				main: function void () {}
		"""
		expect = str(Redeclared(Variable(), "x"))

		self.assertTrue(TestChecker.test(input, expect, 493))

	def test_redeclared_4(self):

		input = r"""
	 a: integer = 5;
	 fn: function integer (a: integer) {
		return a;
	 }
		"""
		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(input, expect, 407))

	def test_redeclared_5(self):

		input = r"""
		fn: function void (x: integer, x: boolean) {
			return;
		}
				main: function void () {}	
		"""

		expect = str(
			Redeclared(Parameter(), "x")
		)

		self.assertTrue(TestChecker.test(input, expect, 497))

	def test_invalid_var1(self):

		input = r"""
		a: integer = 5;
		c: array[2] of integer;
		b: auto;
		main: function void () {}
		"""

		expect = str(Invalid(Variable(), "b"))

		self.assertTrue(TestChecker.test(input, expect, 407))

	def test_invalid_callstmt1(self):

		input = r"""
		c: integer;
	 b: function integer (i : integer) {
		return i;
	 }
	 main: function void () {
		arr: array[2] of integer;
		c = b(arr["1"]);
	 }
		"""

		expect = str(TypeMismatchInExpression(ArrayCell("arr", [StringLit("1")])))
		self.assertTrue(TestChecker.test(input, expect, 490))

	def test_expr_type_mismatch1(self):

		input = r"""
		main: function void () {
			arr: array[2] of integer;
			arr["0"] = 5;
		}
			"""

		expect = str(TypeMismatchInExpression(ArrayCell("arr", [StringLit("0")])))

		self.assertTrue(TestChecker.test(input, expect, 409))

	def test_expr_type_mismatch2(self):

		input = r"""
		main: function void () {
			arr: array[2,2] of integer;
			arr[0,"1"] = 5;
		}
			"""

		expect = str(TypeMismatchInExpression(ArrayCell("arr", [IntegerLit(0), StringLit("1")])))

		self.assertTrue(TestChecker.test(input, expect, 410))

	def test_expr_type_mismatch3(self):

		input = r"""
		main: function void () {
			arr: array[2,2] of integer;
			arr[0,1] = "5";
		}
			"""

		expect = str(TypeMismatchInStatement(AssignStmt(ArrayCell("arr", [IntegerLit(0), IntegerLit(1)]), StringLit("5"))))

		self.assertTrue(TestChecker.test(input, expect, 411))

	def test_expr_type_mismatch4(self):

		input = r"""
		foo: function integer (x: integer) {
			return x;
		}
		main: function void () {
			arr: array[2,2] of integer;
			arr[0,1] = foo(arr);
		}
		"""

		expect = str(TypeMismatchInExpression(FuncCall("foo", [Id("arr")])))

		self.assertTrue(TestChecker.test(input, expect, 412))

	def test_expr_type_mismatch5(self):

		input = r"""
		foo: function string (x: integer) {
			return "123";
		}
		main: function void () {
			arr: array[2,2] of integer;
			arr[0,1] = foo(arr[0,1]);
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(ArrayCell("arr", [IntegerLit(0), IntegerLit(1)]), FuncCall("foo", [ArrayCell("arr", [IntegerLit(0), IntegerLit(1)])]))))

		self.assertTrue(TestChecker.test(input, expect, 413))

	def test_recursive1(self):

		input = r"""
		fn: function integer (x: integer) {
			return fn(x);
		}
		"""

		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(input, expect, 410))

	def test_recursive2(self):

		input = r"""
		fn: function integer (x: string) {
			return fn("avc");
		}
		"""
		expect = str(NoEntryPoint())
		self.assertTrue(TestChecker.test(input, expect, 411))

	def test_array_cell_assign_type_mismatch1(self):

		input=r"""
		main: function void () {
			arr: array[2] of integer;
			arr = 5;
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(Id("arr"), IntegerLit(5))))
		self.assertTrue(TestChecker.test(input, expect, 415))

	def test_array_cell_assign_type_mismatch2(self):

		input = r"""
		a : boolean = true;
		main: function void () {
			arr: array[2,2] of integer;
			a = arr[0,1];
		}
		"""
		expect = str(
			TypeMismatchInStatement(
				AssignStmt(Id("a"), ArrayCell("arr", [IntegerLit(0), IntegerLit(1)]))
			)
		)

		self.assertTrue(TestChecker.test(input, expect, 414))

	def test_arrayLHS_assign_type_mismatch1(self):

		input=r"""
		arr : array[2] of integer;
		main: function void () {
			arr2: array[2] of integer;
			arr  = arr2;
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(Id("arr"), Id("arr2"))))

		self.assertTrue(TestChecker.test(input, expect, 415))

	def test_callstmt_param_type_mismatch1(self):

		input = r"""
		a: function integer (x: integer, y: integer) {
			return x;
		}
		main: function void () {
			a(4, 2.0);
		}
		"""
		expect = str(TypeMismatchInStatement(CallStmt("a", [IntegerLit(4), FloatLit(2.0)])))

		self.assertTrue(TestChecker.test(input, expect, 415))

	def test_callstmt_param_type_mismatch2(self):

		input = r"""
		arr: array[2] of integer;
		a: function integer (x: integer, y: float) {
			return x;
		}
		main: function void () {
			a(4, arr[0]);
		}
		"""
		expect = str(TypeMismatchInStatement(CallStmt("a", [IntegerLit(4), ArrayCell("arr", [IntegerLit(0)])])))

		# self.assertTrue(TestChecker.test(input, expect, 416))

	def test_callstmt_param_type_mismatch3(self):

		input = r"""
		arr: array[2] of integer;
		a: function integer (x: integer, y: array[2] of integer) {
			return x;
		}
		main: function void () {
			a(4, arr[0]);
		}
		"""

		expect = str(TypeMismatchInStatement(CallStmt("a", [IntegerLit(4), ArrayCell("arr", [IntegerLit(0)])])))

		self.assertTrue(TestChecker.test(input, expect, 417))

	def test_callstmt_param_type_mismatch4(self):

		input = r"""
		arr: array[2] of integer;
		a: function integer (x: integer, y: array[2] of integer) {
			return 1;
		}
		main: function void () {
			a(4, arr);
			return c;
		}
		"""

		expect = str(Undeclared(Identifier(), "c"))

		self.assertTrue(TestChecker.test(input, expect, 418))

	def test_implicit_conv_decl(self):

		input=r"""
		a: integer = 5;
		b: float = 5.0;
		c: string = "abc";
		d: boolean = true;
		e: array[2] of integer = {1,2};
		f: array[2,2] of integer = {{1,2},{3,4}};
		g: float = 5;
		h: float = a + 1;
		err: integer = 5.0;
		"""

		expect = str(TypeMismatchInVarDecl(VarDecl("err", IntegerType(), FloatLit(5.0))))

		# self.assertTrue(TestChecker.test(input, expect, 419))

	def test_i2f_2(self):

		input = r"""
		a: integer = 5;
		b: float = 5.0;
		foo: function float (x: float) {
			return x;
		}
		main: function void () {
			b = foo(a);
			a = foo(b);
		}
		"""

		expect = str(
			TypeMismatchInStatement(AssignStmt(Id("a"), FuncCall("foo", [Id("b")])))
		)

		self.assertTrue(TestChecker.test(input, expect, 420))

	def test_auto_decl1(self):

		input = r"""
		foo: function integer (x: integer) {
			return x;
		}
		bar: function integer (x: boolean) {
			return 1;
		}
		zar: function integer (x: float) {
			return 1;
		}
		a: integer = 5;
		e: integer = 7;
		b: auto = 5;
		d: auto = (a + 16) < (17 + e);
		f: auto = 5 + 1.1 + a;
		main: function void () {
			a = foo(b);
			a = b;
			b = bar(d);
			b = zar(f);
			c = foo(b);
		}
		"""
		expect = str(Undeclared(Identifier(), "c"))
		self.assertTrue(TestChecker.test(input, expect, 498))

	#def test_invalid_param1(self):
		
	#	input = r"""
	#	a: integer = 5;
	#	b: function integer (inherit x: integer) {
	#		return x;
	#	}

	#	main: function void () {
	#		a = b(5);
	#	}

	#	"""
	#	expect = str(Invalid(Parameter(), "x"))
	#	self.assertTrue(TestChecker.test(input, expect, 408))

	def test_multi_scope1(self):

		input = r"""
		a: integer = 5;
		foo: function integer (x: integer) {
			b: auto = 5;
			x = 5;
			{
				c: integer = 5;
			}
			{
				c: float = a + 1.1;
			}
			return c;
		}
			main: function void () {}
		"""
				
		expect = str(
			Undeclared(Identifier(), "c")
		)
		self.assertTrue(TestChecker.test(input, expect, 420))


	def test_multi_scope2(self):

		input = r"""
		a: integer = 5;
		foo: function integer (x: integer) {
			b: auto = 5;
			{
				c: integer = 5;
				{
					d: integer = 5;
				}
				c = 6;
				{
					e: integer = 9;
				}
				e  = 10;
			}
			
			return 1;
		}
			main: function void () {}
		"""

		expect = str(Undeclared(Identifier(), "e"))
		self.assertTrue(TestChecker.test(input, expect, 421))
	
	def test_multi_scope3(self):
		
		input = r"""
		a: integer = 5;
		foo: function integer (x: integer) {
			b: auto = 5;
			{
				c: integer = 5;
				{
					d: integer = 5;
				}
				c = 6;
				{
					e: integer = 9;
				}
			}
			
			return 1;
		}
		bar : function integer () {
			a = 5;
			{
				return a;
			}
		}
		
		"""

		expect = str(NoEntryPoint())
		self.assertTrue(TestChecker.test(input, expect, 421))

	def test_forstmt1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
			i : integer;
			for (i = 0, (i+11) < (10+11) , i + 1) {
				i = 5;
			}
			return a;
		}
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 422))

	def test_forstmt2(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 0, i < 10, i + 1) {
				i = 5;
			}
			return i;
		}
			main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "i")
		)
		self.assertTrue(TestChecker.test(input, expect, 423))


	def test_forstmt3(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
			i: integer;
			for (i = 0, i + 10, i + 1) {
				a = a + i;
			}
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(ForStmt(AssignStmt(Id("i"), IntegerLit(0)), BinExpr("+", Id("i"), IntegerLit(10)), BinExpr("+", Id("i"), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("i")))])))
		)
		self.assertTrue(TestChecker.test(input, expect, 424))

	def test_forstmt4(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 1.1, i < 10, i + 1) {
				a = a + i;
			}
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(ForStmt(AssignStmt(Id("i"), FloatLit(1.1)), BinExpr("<", Id("i"), IntegerLit(10)), BinExpr("+", Id("i"), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("i")))])))
		)
		# self.assertTrue(TestChecker.test(input, expect, 425))
	
	def test_forstmt5(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 0, i < 10, i < 1) {
				a = a + i;
			}
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(ForStmt(AssignStmt(Id("i"), IntegerLit(0)), BinExpr("<", Id("i"), IntegerLit(10)), BinExpr("<", Id("i"), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("i")))])))
		)
		# self.assertTrue(TestChecker.test(input, expect, 426))

	def test_ifstmt1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if ((a < 10) && (a > 5)) {
				a = 10;
			}
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 427))

	def test_ifstmt2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a- 10 + 1) {
				a = 10;
			} else {
				a = 5;
			}
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(IfStmt(BinExpr("+", BinExpr("-", Id("a"), IntegerLit(10)), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), IntegerLit(10))]), BlockStmt([AssignStmt(Id("a"), IntegerLit(5))])))
		)
		self.assertTrue(TestChecker.test(input, expect, 428))
	
	def test_ifstmt3(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a < 10) {
				a = 10;
				b : float = 5.5;
			} else {
				a = 5;
				b = 5.5;
			}
			
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 429))
	
	def test_ifstmt4(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a < 10) {
				a = 10;
				c : float = 5.5;
				c = 5.5;
			} else {
				a = 5;
				b : float = 5.5;
			}
			b = 5.5;
			
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 430))
	
	def test_ifstmt5(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a < 10) 
				a = 10;
			 else {
				a = 5;
				b : float = 5.5;
				b = 5.5;
			}
			
			return b;
		}
		main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 431))

	
	def test_whileStmt1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
			}
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 432))
	
	def test_whileStmt2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while ((11 > a) && (10 - 1 < 1)) 
				a = 10;
				b : float = 5.5;
			
		b = .e1;
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 433))
	

	def test_dowhile1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			do {
				a = 10;
			} while (a < 10);
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 434))
	
	def test_dowhile2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			do {
				a = 10;
				b : float = 5.5;
			} while (a - 10);
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(DoWhileStmt(BinExpr("-", Id("a"), IntegerLit(10)), BlockStmt([AssignStmt(Id("a"), IntegerLit(10)), VarDecl("b", FloatType(), FloatLit(5.5))])))
		)
		self.assertTrue(TestChecker.test(input, expect, 435))
	
	def test_break1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
				break;
			}
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 436))
	
	def test_break2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
				break;
				b : float = 5.5;
			}
			break;
			return a;
		}	main: function void () {}
	
		"""

		expect = str(
			MustInLoop(BreakStmt())
		)
		self.assertTrue(TestChecker.test(input, expect, 437))
	

	def test_continue1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
				continue;
			}
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 438))

	def test_continue2(self):
		
		input = r"""
		a : integer = 5;
		c : boolean = true;
		foo: function integer (x: integer) {
		
			while (!c) {
				a = 10;
				continue;
				b : float = 5.5;
			}
			continue;
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			MustInLoop(ContinueStmt())
		)
		self.assertTrue(TestChecker.test(input, expect, 439))


	def test_arraylit1(self):

		input = r"""
		b: auto = {1, 2, 3, 4, 5};
		a : array[5] of integer = {1, 2, 3, 4, 5.5};
		
		foo: function integer (x: integer) {
			return 1;
		}
		main: function void () {}
		"""

		expect = str(
			IllegalArrayLiteral(ArrayLit([IntegerLit(1), IntegerLit(2), IntegerLit(3), IntegerLit(4), FloatLit(5.5)]))
		)
		self.assertTrue(TestChecker.test(input, expect, 497))

	def test_arraylit2(self):
		
		input = r"""
		b: auto = {1, 2, 3, 4, 5};
		a : array[3,2] of integer = {{1, 2}, {3, 4}, {5.5, 6}};
		
		foo: function integer (x: integer) {
			return 1;
		}
		main: function void () {}
		"""

		expect = str(
			IllegalArrayLiteral(ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4)]), ArrayLit([FloatLit(5.5), IntegerLit(6)])]))
		)
		self.assertTrue(TestChecker.test(input, expect, 489))

	
	def test_arraylit3(self):

		input = r"""
		b: auto = {1, 2, 3, 4, 5};
		a : array[3,2] of integer = {{1, 2}, {3, 4}, {5.5}};
		
		foo: function integer (x: integer) {
			return 1;
		}
		main: function void () {}
		"""

		expect = str(
			IllegalArrayLiteral(ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4)]), ArrayLit([FloatLit(5.5)])]))
		)
		self.assertTrue(TestChecker.test(input, expect, 490))

	def test_arraylit4(self):
		
		input = r"""
		a : array[3,2] of integer = {{1, 2}, {3, 4}, {5, 6}};
		
		foo: function integer (x: array[3,2] of integer) {
			return 1;
		}
		main: function void () {
			foo({{1, 2}, {3, 4}, {5, 6}}); // infer array
			foo(b);
		}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 491))	

	def test_binexpr1(self):

		input = r"""
		a : integer = 5;
		b : integer = 10;
		c : integer = a + b;
		d : integer = a - b;
		e : integer = a * b;
		f : integer = a / b;
		g : integer = a % b;
		h : boolean = a && b;
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(BinExpr("&&", Id("a"), Id("b")))
		)
		self.assertTrue(TestChecker.test(input, expect, 494))

	def test_i2f_1(self):
		
		input = r"""
		a : integer = 5;
		b : float = 10.5;
		c : float = a + b;
		d : float = a - b;
		e : float = a * b;
		f : float = a / b;
		g : float = a % b;
		h : boolean = a <= b;
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(BinExpr("%", Id("a"), Id("b")))
		)
		self.assertTrue(TestChecker.test(input, expect, 491))

	def test_array_subscript1(self):
		
		input = r"""
		a : array[5] of integer = {1, 2, 3, 4, 5};
		b : integer = a[5];
		c : integer = a[6];
		d : integer = a[0];
		e : integer = a[-1];
		f : integer = a[1.5];
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(ArrayCell("a", [FloatLit(1.5)]))
		)
		self.assertTrue(TestChecker.test(input, expect, 489))
	
	def test_array_subscript2(self):
		
		input = r"""
		a : integer = 5;
		b : integer = a[5];
		c : integer = a[6];
		d : integer = a[0];
		e : integer = a[-1];
		f : integer = a[1.5];
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(ArrayCell("a", [IntegerLit(5)]))
		)
		self.assertTrue(TestChecker.test(input, expect, 479))

	def test_ifstmt6(self):
		
		input = r"""
		a : integer = 5;
		b : integer = 10;
		c : integer = a + b;
		d : integer = a - b;
		e : integer = a * b;
		main : function void () {
			if (a + b)  {
				a = 10;
			} else {
				a = 5;
			}
		}
		"""

		expect = str(
			TypeMismatchInStatement(IfStmt(
				cond=BinExpr("+", Id("a"), Id("b")),
				tstmt=BlockStmt([AssignStmt(Id("a"), IntegerLit(10))]),
				fstmt=BlockStmt([AssignStmt(Id("a"), IntegerLit(5))]),
			))
		)

		self.assertTrue(TestChecker.test(input, expect, 459))
	
	#def test_auto1(self):

	#	input = r"""

	#	"""

	def test_return1(self):
		
		input = r"""
		f : function float () {
			return 1;
		}
		b: function boolean () {
			return 2;
		}
		main : function void () {
			return;
		}
		"""

		expect = str(
			TypeMismatchInStatement(ReturnStmt(IntegerLit(2)))
		)

		self.assertTrue(TestChecker.test(input, expect, 458))

	def test_vardecl1(self):

		input = r"""
		a: integer = 1.1;
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInVarDecl(VarDecl("a", IntegerType(), FloatLit(1.1)))
		)

		self.assertTrue(TestChecker.test(input, expect, 457))

	def test_operand1(self):

		input = r"""
		foo: function auto () {
	
		}
		bar: function integer () {
			return 1;
		}
		a: boolean = foo() == bar();
		main : function void () {
			a = false;
			b = true;
		}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)

		self.assertTrue(TestChecker.test(input, expect, 455))

	def test_operand2(self):

		input = r"""
		main: function void () {
			a: integer = 1;
			a = 12.2 % 2;
			}
		"""

		expect = str(
			TypeMismatchInExpression(BinExpr("%", FloatLit(12.2), IntegerLit(2)))	
		)

		self.assertTrue(TestChecker.test(input, expect, 454))
	def test_func_inherit(self):
		inp = r"""
		m: function integer () inherit a {
			return 1;
		}
		main: function void () {
			a: integer = 1;
		}
		"""
		expect = str(Undeclared(Function(), "a"))
		self.assertTrue(TestChecker.test(inp, expect, 453))
	def test_parameter(self):
		inp = r"""
		m: function integer (b: integer) inherit a {
			super(1);
			return 1;
		}
		main: function void () {
			a: integer = 1;
		}
		a: function integer (inherit b: integer) {
		}
		"""
		expect= str(Invalid(Parameter(), "b"))
		self.assertTrue(TestChecker.test(inp, expect, 451))
	def test_parameter_auto(self):
		inp = r"""
		a: integer = m(1);
		b: integer = m(1.1);
		m: function integer (b: auto){
			return 1;
		}
		main: function void () {}
		"""
		expect= str(
			TypeMismatchInExpression(FuncCall("m", [FloatLit(1.1)]))
		)
		self.assertTrue(TestChecker.test(inp, expect, 450))
	def test_parameter_auto1(self):
		inp = r"""
		m: function integer (b: auto){
			return b + 1;
		}
		a: integer = m(1.1);
		
		main: function void () {}
		"""
		expect= str(
			TypeMismatchInExpression(FuncCall("m", [FloatLit(1.1)]))
		)
		self.assertTrue(TestChecker.test(inp, expect, 449))
	def test_parameter_auto2(self):
		inp = r"""
		m: function integer (b: auto){
			return b > 1;
		}
		a: integer = m(1);
		
		main: function void () {}
		"""
		expect= str(
			TypeMismatchInStatement(ReturnStmt(BinExpr(">", Id("b"), IntegerLit(1))))
		)
		self.assertTrue(TestChecker.test(inp, expect, 448))
	def test_parameter_auto2(self):
		inp = r"""
		m: function auto (b: auto){
			return b > 1;
		}
		a: integer = m(1);
		
		main: function void () {}
		"""
		expect= str(
			TypeMismatchInVarDecl(VarDecl("a", IntegerType(), FuncCall("m", [IntegerLit(1)])))
		)
		self.assertTrue(TestChecker.test(inp, expect, 447))
	def test_parameter_auto2(self):
		inp = r"""
		a: integer = m(1);
		m: function float (b: auto){
			return b + 1;
		}
		
		main: function void () {}
		"""
		expect= str(
			TypeMismatchInVarDecl(VarDecl("a", IntegerType(), FuncCall("m", [IntegerLit(1)])))
		)
		self.assertTrue(TestChecker.test(inp, expect, 447))
	def test_inherit(self):
		inp = r"""
		m: function auto (inherit b: auto){
			return b;
		}
		b: function integer (b: integer) inherit m {
			preventDefault();
			a: auto;
		}
		main: function void () {}
		"""
		expect = str(Invalid(Variable(), "a"))
		self.assertTrue(TestChecker.test(inp, expect, 446))
	def test_expresion_out(self):
		inp = r"""
		c: function integer () {
		}
		m: function auto (inherit b: auto){
			a: integer = 1+ 2 + m(25) + 6/5;
			b = (a - c())> 5;
			return b;
        }
		main: function void () {}
		"""
		expect = str(TypeMismatchInStatement(AssignStmt(Id("b"), BinExpr(">", BinExpr("-", Id("a"), FuncCall("c", [])), IntegerLit(5)))))
		self.assertTrue(TestChecker.test(inp, expect, 445))
	def test_parameter_implicit(self):
		inp = r"""
		m: function auto (b: float){
		}
		main: function void () {
			a: integer = m(1);
			v: auto;
		}
		"""
		expect = str(Invalid(Variable(), "v"))
		self.assertTrue(TestChecker.test(inp, expect, 444))
	def test_function(self):
		inp = r"""
		m: function integer (b: integer){
		}
		m2: function integer (b: integer){
			{
				m: integer = 5;
			}
		}
		main: function void () {}
		"""
		expect = str(Redeclared(Variable(), "m"))
		self.assertTrue(TestChecker.test(inp, expect, 443))

	def test_no_entry1(self):

		inp=r"""
		a: integer;
		b: function integer (x: integer) {
			return x;
		}
		c: boolean;
		"""

		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(inp, expect, 400))

	def test_no_entry2(self):

		inp=r"""
		a: integer;

		c: boolean;
		"""
		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(inp, expect, 401))

	def test_vardecl2(self):

		input = r"""
			a: array [5] of integer = {1};
			main: function void () {}
		"""

		expect = str(
			TypeMismatchInVarDecl(VarDecl("a", ArrayType([5], IntegerType()), ArrayLit([IntegerLit(1)])))
			)

		self.assertTrue(TestChecker.test(input, expect, 469))
		
		# TODO invalid array or type mismatch?

	def test_undeclared_1(self):

		input = r"""
		a1: integer = 5;
		b: function integer (x: integer) {
			c: integer;
			x = 1;
			return a;
		}
				main: function void () {}

		"""

		expect = str(Undeclared(Identifier(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 401))

	def test_undeclared_2(self):

		input = r"""
		a: integer = 5;
		b: function integer (x: integer) {
			x = a;
			return c;
		}
				main: function void () {}

		"""
		expect = str(Undeclared(Identifier(), "c"))

		self.assertTrue(TestChecker.test(input, expect, 402))

	def test_undeclared_3(self):

		input = r"""
		a1: integer = 5;
		b: function integer (x: integer) {
			x = 1;
			{
				c: integer = 5;
				{
					return a;
				}
			}
		}
				main: function void () {}

		"""

		expect = str(Undeclared(Identifier(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 403))

	def test_undeclared_4(self):

		input = r"""
		a: integer = 5;
		b: function integer (x: integer) {
			return c(x);
		}
				main: function void () {}

		"""

		expect = str(Undeclared(Function(), "c"))

		self.assertTrue(TestChecker.test(input, expect, 402))

	def test_undeclared_5(self):

		input = r"""
		c: function integer (d: boolean) {
			return 9;
		}
		a: integer = 5;
		b: function integer (x: integer) {
			return c(d);
		}
				main: function void () {}

		"""
		expect = str(Undeclared(Identifier(), "d"))

		self.assertTrue(TestChecker.test(input, expect, 402))

	def test_undeclared_6(self):

		input = r"""
		c: function integer (d: boolean, e: integer) {
			return 3;
		}
		a: integer = 5;
		b: function integer (x: integer) {
			return c(true, e);
		}
				main: function void () {}

		"""

		expect = str(Undeclared(Identifier(), "e"))

		self.assertTrue(TestChecker.test(input, expect, 405))

	def test_return2(self):

		input = r"""
		d: boolean = true;
		c: function boolean (d: boolean) {
			return d;
		}
		a: integer = 5;
		b: function integer (x: integer) {
			return c(d);
		}
				main: function void () {}
		"""

		expect = str(TypeMismatchInStatement(ReturnStmt(FuncCall("c", [Id("d")]))))

		self.assertTrue(TestChecker.test(input, expect, 495))

	def test_return3(self):

		input = r"""
		d: boolean = true;
		c: function auto (d: boolean) {
			return d;
		}
		a: boolean = true;
		b: function boolean (x: integer) {
			return c(a);
		}
		//		main: function void () {}
		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 491))
	
	def test_return4(self):
		
		input = r"""
		a: integer = 1;
		c: function auto (d: float) {
			return d;
		}
	
		main: function void () {
			a = 1 + c(1.0);

		}
		"""

		expect = str(
			TypeMismatchInStatement(AssignStmt(Id("a"), BinExpr("+", IntegerLit(1), FuncCall("c", [FloatLit(1.0)]))))
		)

		self.assertTrue(TestChecker.test(input, expect, 490))

	def test_return5(self):
		
		input = r"""
		a: array [2] of integer;
		c: function auto (d: float) {
			return d;
		}
	
		main: function void () {
			a[0] = 1 + c(1.0);

		}
		"""

		expect = str(
			TypeMismatchInStatement(AssignStmt(ArrayCell("a", [IntegerLit(0)]), BinExpr("+", IntegerLit(1), FuncCall("c", [FloatLit(1.0)]))))
		)

		self.assertTrue(TestChecker.test(input, expect, 498))

	def test_auto_func1(self):

		input = r"""
		foo : function auto ( a : integer , b : integer ) {}
		a : float = foo (1 , 2 ) ;
		b : integer = foo (1 , 2) + 1;

		main: function void () { foo(1, 2); }
  		"""
		expect = str(
			TypeMismatchInVarDecl(VarDecl("b", IntegerType(), BinExpr("+", FuncCall("foo", [IntegerLit(1), IntegerLit(2)]), IntegerLit(1))))
		)

		self.assertTrue(TestChecker.test(input, expect, 479))
		# TODO edge cases

	def test_auto_func2(self):
		
		input = r"""
		foo : function auto ( a : integer , b : integer ) {}
		b : integer = foo (1 , 2) + 1;
		a : float = foo (1 , 2 ) ;
  		"""
		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 492))



	def test_redeclared_1(self):

		input = r"""
		a: integer = 5;
		b: integer = 6;
		a: integer = 6;
				main: function void () {}

		"""

		expect = str(Redeclared(Variable(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 404))

	def test_redeclared_2(self):

		input = r"""
		fn: function integer (x: integer) {
			return x;
			}
			fn: function integer (x: integer) {
				return x;
				}
		main: function void () {}
		"""

		expect = str(Redeclared(Function(), "fn"))

		self.assertTrue(TestChecker.test(input, expect, 405))

	def test_redeclared_3(self):

		input = r"""
		fn: function void (x: integer) {
			x: integer = 5;
			return;
		}
				main: function void () {}

		"""
		expect = str(Redeclared(Variable(), "x"))

		self.assertTrue(TestChecker.test(input, expect, 493))

	def test_redeclared_4(self):

		input = r"""
	 a: integer = 5;
	 fn: function integer (a: integer) {
		return a;
	 }
		"""
		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(input, expect, 407))

	def test_redeclared_5(self):

		input = r"""
		fn: function void (x: integer, x: boolean) {
			return;
		}
				main: function void () {}	
		"""

		expect = str(
			Redeclared(Parameter(), "x")
		)

		self.assertTrue(TestChecker.test(input, expect, 497))

	def test_invalid_var1(self):

		input = r"""
		a: integer = 5;
		c: array[2] of integer;
		b: auto;
		main: function void () {}

		"""

		expect = str(Invalid(Variable(), "b"))

		self.assertTrue(TestChecker.test(input, expect, 407))

	def test_invalid_callstmt1(self):

		input = r"""
		c: integer;
	 b: function integer (i : integer) {
		return i;
	 }
	 main: function void () {
		arr: array[2] of integer;
		c = b(arr["1"]);
	 }
		"""

		expect = str(TypeMismatchInExpression(ArrayCell("arr", [StringLit("1")])))
		self.assertTrue(TestChecker.test(input, expect, 490))

	def test_param1(self):

		input = r"""
		a: integer = 5;
		b: function float (i : float) {
			return i;
		}
		main: function void () {
			b(a);
			b(1);
			a(1);
		}
		"""

		expect = str(Undeclared(Function(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 408))

	def test_param2(self):
		
		input = r"""
	
		a: integer = 5;
		i: float = 5;
		b: function integer (i : auto) {
			return 12 % (i + 1) + d(5);
		}
		main: function void () {
			b(a);
			b(1);
			a(1);
		}
		d: function integer (i : integer) {
			return i;
		}
		"""

		expect = str(Undeclared(Function(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 498))

	def test_param3(self):
		
		input = r"""
		a: integer = 5;
		b: function string (i : auto) {
			return i;
		}
		main: function void () {
			b(a);
		}
		"""

		expect = str(TypeMismatchInStatement(CallStmt("b", [Id("a")])))

		self.assertTrue(TestChecker.test(input, expect, 493))

	def test_param4(self):
		
		input = r"""
		a: integer = 5;
		b: function auto (i : auto) {
			return i;
		}
		main: function void () {
			b(a);
			b(1);
			a(1);
		}
		"""

		expect = str(Undeclared(Function(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 479))

	def test_param4point5(self):
		
		input = r"""
		a: integer = 5;
		b: function auto (i : auto) {
			return i;
		}
		main: function void () {
			a = b(a) + 1.5;
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(Id("a"), BinExpr("+", FuncCall("b", [Id("a")]), FloatLit(1.5)))))

		self.assertTrue(TestChecker.test(input, expect, 500))
	
	def test_param5(self):

		input = r"""
		a: array [2] of integer;
		b: function integer (a : array [2] of integer) {
			return a[1];
		}
		main: function void () {
			b(a);
			a(1);
		}
		"""

		expect = str(Undeclared(Function(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 409))

	def test_return6(self):

		input = r"""
			a: float = foo(1, 2) + 1.5;
			foo: function auto(a: integer, b: integer) {
				return a + b;
			}
			b: float = foo(1, 2);
		"""
		
		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 498))

	#def test_param5(self):

	#	input = r"""
	#	a: integer = 5;
	
	#	foo: function auto (i : auto) {
	#		return i;
	#	}

	#	b: function integer (i : integer) {
	#		return foo(5.6);
	#	}
	#	"""

	#	expect = str(TypeMismatchInExpression(FuncCall("foo", [])))

	def test_param6(self):

		input = r"""
		a: integer = 5;
		b: function auto (i : float) {
			return i;
		}
		main: function void () {
			b(a);
			a(1);
		}

		"""

		expect = str(Undeclared(Function(), "a"))

		self.assertTrue(TestChecker.test(input, expect, 409))


	def test_expr_type_mismatch1(self):

		input = r"""

		main: function void () {
			arr: array[2] of integer;
			arr["0"] = 5;
		}
			"""

		expect = str(TypeMismatchInExpression(ArrayCell("arr", [StringLit("0")])))

		self.assertTrue(TestChecker.test(input, expect, 409))

	def test_expr_type_mismatch2(self):

		input = r"""

		main: function void () {
			arr: array[2,2] of integer;
			arr[0,"1"] = 5;
		}
			"""

		expect = str(TypeMismatchInExpression(ArrayCell("arr", [IntegerLit(0), StringLit("1")])))

		self.assertTrue(TestChecker.test(input, expect, 410))

	def test_expr_type_mismatch3(self):

		input = r"""

		main: function void () {
			arr: array[2,2] of integer;
			arr[0,1] = "5";
		}
			"""

		expect = str(TypeMismatchInStatement(AssignStmt(ArrayCell("arr", [IntegerLit(0), IntegerLit(1)]), StringLit("5"))))

		self.assertTrue(TestChecker.test(input, expect, 411))

	def test_expr_type_mismatch4(self):

		input = r"""
		foo: function integer (x: integer) {
			return x;
		}
		main: function void () {
			arr: array[2,2] of integer;
			arr[0,1] = foo(arr);
		}
		"""

		expect = str(TypeMismatchInExpression(FuncCall("foo", [Id("arr")])))

		self.assertTrue(TestChecker.test(input, expect, 412))

	def test_expr_type_mismatch5(self):

		input = r"""
		foo: function string (x: integer) {
			return "123";
		}
		main: function void () {
			arr: array[2,2] of integer;
			arr[0,1] = foo(arr[0,1]);
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(ArrayCell("arr", [IntegerLit(0), IntegerLit(1)]), FuncCall("foo", [ArrayCell("arr", [IntegerLit(0), IntegerLit(1)])]))))

		self.assertTrue(TestChecker.test(input, expect, 413))

	#def test_super_call1(self):

	#	input = r"""

	#	"""

	def test_recursive1(self):

		input = r"""
		fn: function integer (x: integer) {
			return fn(x);
		}
		"""

		expect = str(NoEntryPoint())

		self.assertTrue(TestChecker.test(input, expect, 410))

	def test_recursive2(self):

		input = r"""
		fn: function integer (x: string) {
			return fn("avc");
		}

		"""
		expect = str(NoEntryPoint())
		self.assertTrue(TestChecker.test(input, expect, 411))

	def test_array_cell_assign_type_mismatch1(self):

		input=r"""
		main: function void () {
			arr: array[2] of integer;
			arr = 5;
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(Id("arr"), IntegerLit(5))))
		self.assertTrue(TestChecker.test(input, expect, 415))

	def test_array_cell_assign_type_mismatch2(self):

		input = r"""
		a : boolean = true;
		main: function void () {
			arr: array[2,2] of integer;
			a = arr[0,1];
		}
		"""
		expect = str(
			TypeMismatchInStatement(
				AssignStmt(Id("a"), ArrayCell("arr", [IntegerLit(0), IntegerLit(1)]))
			)
		)

		self.assertTrue(TestChecker.test(input, expect, 414))

	def test_arrayLHS_assign_type_mismatch1(self):

		input=r"""
		arr : array[2] of integer;
		main: function void () {
			arr2: array[2] of integer;
			arr  = arr2;
		}
		"""

		expect = str(TypeMismatchInStatement(AssignStmt(Id("arr"), Id("arr2"))))

		self.assertTrue(TestChecker.test(input, expect, 415))

	def test_callstmt_param_type_mismatch1(self):

		input = r"""
		a: function integer (x: integer, y: integer) {
			return x;
		}
		main: function void () {
			a(4, 2.0);
		}
		"""
		expect = str(TypeMismatchInStatement(CallStmt("a", [IntegerLit(4), FloatLit(2.0)])))

		self.assertTrue(TestChecker.test(input, expect, 415))

	def test_callstmt_param_type_mismatch2(self):

		input = r"""
		arr: array[2] of integer;
		a: function integer (x: integer, y: float) {
			return x;
		}
		main: function void () {

			a(4, arr[0]);
		}
		"""
		expect = str(TypeMismatchInStatement(CallStmt("a", [IntegerLit(4), ArrayCell("arr", [IntegerLit(0)])])))

		# self.assertTrue(TestChecker.test(input, expect, 416))

	def test_callstmt_param_type_mismatch3(self):

		input = r"""
		arr: array[2] of integer;
		a: function integer (x: integer, y: array[2] of integer) {
			return x;
		}
		main: function void () {

			a(4, arr[0]);
		}
		"""

		expect = str(TypeMismatchInStatement(CallStmt("a", [IntegerLit(4), ArrayCell("arr", [IntegerLit(0)])])))

		self.assertTrue(TestChecker.test(input, expect, 417))

	def test_callstmt_param_type_mismatch4(self):

		input = r"""
		arr: array[2] of integer;
		a: function integer (x: integer, y: array[2] of integer) {
			return 1;
		}
		main: function void () {

			a(4, arr);
			return c;
		}
		"""

		expect = str(Undeclared(Identifier(), "c"))

		self.assertTrue(TestChecker.test(input, expect, 418))

	def test_implicit_conv_decl(self):

		input=r"""
		a: integer = 5;
		b: float = 5.0;
		c: string = "abc";
		d: boolean = true;
		e: array[2] of integer = {1,2};
		f: array[2,2] of integer = {{1,2},{3,4}};

		g: float = 5;
		h: float = a + 1;
		err: integer = 5.0;
		"""

		expect = str(TypeMismatchInVarDecl(VarDecl("err", IntegerType(), FloatLit(5.0))))

		self.assertTrue(TestChecker.test(input, expect, 419))

	def test_i2f_2(self):

		input = r"""
		a: integer = 5;
		b: float = 5.0;
		foo: function float (x: float) {
			return x;
		}
		main: function void () {
			b = foo(a);
			a = foo(b);
		}

		"""

		expect = str(
			TypeMismatchInStatement(
				AssignStmt(Id("a"), FuncCall("foo", [Id("b")]))
			)
		)

		self.assertTrue(TestChecker.test(input, expect, 420))

	def test_i2f_3(self):
		
		input = r"""
		a: integer = 5;
		b: float = 5.0;
		foo: function float (x: float) {
			return x;
		}
		main: function void () {
			b = foo(a);
			c = foo(b);
		}

		"""

		expect = str(
			
			Undeclared(Identifier(), "c")
		)

		self.assertTrue(TestChecker.test(input, expect, 421))

	def test_auto_decl1(self):

		input = r"""
		foo: function integer (x: integer) {
			return x;
		}

		bar: function integer (x: boolean) {
			return 1;
		}

		zar: function integer (x: float) {
			return 1;
		}

		a: integer = 5;
		e: integer = 7;
		b: auto = 5;
		d: auto = (a + 16) < (17 + e);
		f: auto = 5 + 1.1 + a;
		main: function void () {
			a = foo(b);

			a = b;

			b = bar(d);

			b = zar(f);

			c = foo(b);
		}
		"""
		expect = str(Undeclared(Identifier(), "c"))
		self.assertTrue(TestChecker.test(input, expect, 498))

	#def test_invalid_param1(self):
		
	#	input = r"""
	#	a: integer = 5;
	#	b: function integer (inherit x: integer) {
	#		return x;
	#	}

	#	main: function void () {
	#		a = b(5);
	#	}

	#	"""
	#	expect = str(Invalid(Parameter(), "x"))
	#	self.assertTrue(TestChecker.test(input, expect, 408))

	def test_multi_scope1(self):

		input = r"""
		a: integer = 5;
		foo: function integer (x: integer) {
			b: auto = 5;
			x = 5;
			{
				c: integer = 5;
			}
			{
				c: float = a + 1.1;
			}

			return c;
		}
			main: function void () {}
		"""
				
		expect = str(
			Undeclared(Identifier(), "c")
		)
		self.assertTrue(TestChecker.test(input, expect, 420))


	def test_multi_scope2(self):

		input = r"""
		a: integer = 5;
		foo: function integer (x: integer) {
			b: auto = 5;
			{
				c: integer = 5;
				{
					d: integer = 5;
				}
				c = 6;
				{
					e: integer = 9;
				}
				e  = 10;
			}
			
			return 1;
		}
			main: function void () {}
		"""

		expect = str(Undeclared(Identifier(), "e"))
		self.assertTrue(TestChecker.test(input, expect, 421))
	
	def test_multi_scope3(self):
		
		input = r"""
		a: integer = 5;
		foo: function integer (x: integer) {
			b: auto = 5;
			{
				c: integer = 5;
				{
					d: integer = 5;
				}
				c = 6;
				{
					e: integer = 9;
				}
			}
			
			return 1;
		}
		bar : function integer () {
			a = 5;
			{
				return a;
			}
		}
		
		"""

		expect = str(NoEntryPoint())
		self.assertTrue(TestChecker.test(input, expect, 421))

	def test_forstmt1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 0, (i+11) < (10+11) , i + 1) {
				i = 5;
			}

			return a;
		}
		"""

		expect = str(
			NoEntryPoint()
		)
		# self.assertTrue(TestChecker.test(input, expect, 422))

	def test_forstmt2(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 0, i < 10, i + 1) {
				i = 5;
			}

			return i;
		}
			main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "i")
		)
		self.assertTrue(TestChecker.test(input, expect, 423))


	def test_forstmt3(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 0, i + 10, i + 1) {
				a = a + i;
			}

			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(ForStmt(AssignStmt(Id("i"), IntegerLit(0)), BinExpr("+", Id("i"), IntegerLit(10)), BinExpr("+", Id("i"), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("i")))])))
		)
		# self.assertTrue(TestChecker.test(input, expect, 424))

	def test_forstmt4(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 1.1, i < 10, i + 1) {
				a = a + i;
			}

			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(ForStmt(AssignStmt(Id("i"), FloatLit(1.1)), BinExpr("<", Id("i"), IntegerLit(10)), BinExpr("+", Id("i"), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("i")))])))
		)
		# self.assertTrue(TestChecker.test(input, expect, 425))
	
	def test_forstmt5(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			for (i = 0, i < 10, i < 1) {
				a = a + i;
			}

			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(ForStmt(AssignStmt(Id("i"), IntegerLit(0)), BinExpr("<", Id("i"), IntegerLit(10)), BinExpr("<", Id("i"), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("i")))])))
		)
		# self.assertTrue(TestChecker.test(input, expect, 426))

	def test_ifstmt1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if ((a < 10) && (a > 5)) {
				a = 10;
			}

			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 427))

	def test_ifstmt2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a- 10 + 1) {
				a = 10;
			} else {
				a = 5;
			}

			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(IfStmt(BinExpr("+", BinExpr("-", Id("a"), IntegerLit(10)), IntegerLit(1)), BlockStmt([AssignStmt(Id("a"), IntegerLit(10))]), BlockStmt([AssignStmt(Id("a"), IntegerLit(5))])))
		)
		self.assertTrue(TestChecker.test(input, expect, 428))
	
	def test_ifstmt3(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a < 10) {
				a = 10;
				b : float = 5.5;
			} else {
				a = 5;
				b = 5.5;
			}
			
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 429))
	
	def test_ifstmt4(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a < 10) {
				a = 10;
				c : float = 5.5;
				c = 5.5;
			} else {
				a = 5;
				b : float = 5.5;
			}
			b = 5.5;
			
			return a;
		}
		main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 430))
	
	def test_ifstmt5(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			if (a < 10) 
				a = 10;
			 else {
				a = 5;
				b : float = 5.5;
				b = 5.5;
			}
			
			return b;
		}
		main: function void () {}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 431))

	
	def test_whileStmt1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
			}

			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 432))
	
	def test_whileStmt2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while ((11 > a) && (10 - 1 < 1)) 
				a = 10;
				b : float = 5.5;
			
		b = .e1;
			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 433))
	

	def test_dowhile1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			do {
				a = 10;
			} while (a < 10);

			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 434))
	
	def test_dowhile2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			do {
				a = 10;
				b : float = 5.5;
			} while (a - 10);

			return a;
		}
		main: function void () {}
		"""

		expect = str(
			TypeMismatchInStatement(DoWhileStmt(BinExpr("-", Id("a"), IntegerLit(10)), BlockStmt([AssignStmt(Id("a"), IntegerLit(10)), VarDecl("b", FloatType(), FloatLit(5.5))])))
		)
		self.assertTrue(TestChecker.test(input, expect, 435))
	
	def test_break1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
				break;
			}

			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 436))
	
	def test_break2(self):
		
		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
				break;
				b : float = 5.5;
			}
			break;

			return a;
		}	main: function void () {}
	
		"""

		expect = str(
			MustInLoop(BreakStmt())
		)
		self.assertTrue(TestChecker.test(input, expect, 437))
	

	def test_continue1(self):

		input = r"""
		a : integer = 5;
		foo: function integer (x: integer) {
		
			while (a < 10) {
				a = 10;
				continue;
			}

			return a;
		}
	
		"""

		expect = str(
			NoEntryPoint()
		)
		self.assertTrue(TestChecker.test(input, expect, 438))

	def test_continue2(self):
		
		input = r"""
		a : integer = 5;
		c : boolean = true;
		foo: function integer (x: integer) {
		
			while (!c) {
				a = 10;
				continue;
				b : float = 5.5;
			}
			continue;

			return a;
		}
		main: function void () {}
		"""

		expect = str(
			MustInLoop(ContinueStmt())
		)
		self.assertTrue(TestChecker.test(input, expect, 439))


	def test_arraylit1(self):

		input = r"""
		b: auto = {1, 2, 3, 4, 5};
		a : array[5] of integer = {1, 2, 3, 4, 5.5};
		
		foo: function integer (x: integer) {

			return 1;
		}
		main: function void () {}
		"""

		expect = str(
			IllegalArrayLiteral(ArrayLit([IntegerLit(1), IntegerLit(2), IntegerLit(3), IntegerLit(4), FloatLit(5.5)]))
		)
		self.assertTrue(TestChecker.test(input, expect, 497))

	def test_arraylit2(self):
		
		input = r"""
		b: auto = {1, 2, 3, 4, 5};
		a : array[3,2] of integer = {{1, 2}, {3, 4}, {5.5, 6}};
		
		foo: function integer (x: integer) {

			return 1;
		}
		main: function void () {}
		"""

		expect = str(
			IllegalArrayLiteral(ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4)]), ArrayLit([FloatLit(5.5), IntegerLit(6)])]))
		)
		self.assertTrue(TestChecker.test(input, expect, 489))

	
	def test_arraylit3(self):

		input = r"""
		b: auto = {1, 2, 3, 4, 5};
		a : array[3,2] of integer = {{1, 2}, {3, 4}, {5.5}};
		
		foo: function integer (x: integer) {

			return 1;
		}
		main: function void () {}
		"""

		expect = str(
			IllegalArrayLiteral(ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)]), ArrayLit([IntegerLit(3), IntegerLit(4)]), ArrayLit([FloatLit(5.5)])]))
		)
		self.assertTrue(TestChecker.test(input, expect, 490))

	def test_arraylit4(self):
		
		input = r"""
		a : array[3,2] of integer = {{1, 2}, {3, 4}, {5, 6}};
		
		foo: function integer (x: array[3,2] of integer) {

			return 1;
		}
		main: function void () {
			foo({{1, 2}, {3, 4}, {5, 6}}); // infer array
			foo(b);
		}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)
		self.assertTrue(TestChecker.test(input, expect, 491))	

	def test_binexpr1(self):

		input = r"""
		a : integer = 5;
		b : integer = 10;
		c : integer = a + b;
		d : integer = a - b;
		e : integer = a * b;
		f : integer = a / b;
		g : integer = a % b;
		h : boolean = a && b;

		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(BinExpr("&&", Id("a"), Id("b")))
		)
		self.assertTrue(TestChecker.test(input, expect, 494))

	def test_i2f_1(self):
		
		input = r"""
		a : integer = 5;
		b : float = 10.5;
		c : float = a + b;
		d : float = a - b;
		e : float = a * b;
		f : float = a / b;
		g : float = a % b;
		h : boolean = a <= b;

		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(BinExpr("%", Id("a"), Id("b")))
		)
		self.assertTrue(TestChecker.test(input, expect, 491))

	def test_array_subscript1(self):
		
		input = r"""
		a : array[5] of integer = {1, 2, 3, 4, 5};
		b : integer = a[5];
		c : integer = a[6];
		d : integer = a[0];
		e : integer = a[-1];
		f : integer = a[1.5];

		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(ArrayCell("a", [FloatLit(1.5)]))
		)
		self.assertTrue(TestChecker.test(input, expect, 489))
	
	def test_array_subscript2(self):
		
		input = r"""
		a : integer = 5;
		b : integer = a[5];
		c : integer = a[6];
		d : integer = a[0];
		e : integer = a[-1];
		f : integer = a[1.5];

		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(ArrayCell("a", [IntegerLit(5)]))
		)
		self.assertTrue(TestChecker.test(input, expect, 479))

	def test_ifstmt6(self):
		
		input = r"""
		a : integer = 5;
		b : integer = 10;
		c : integer = a + b;
		d : integer = a - b;
		e : integer = a * b;

		main : function void () {
			if (a + b)  {
				a = 10;
			} else {
				a = 5;
			}
		}
		"""

		expect = str(
			TypeMismatchInStatement(IfStmt(
				cond=BinExpr("+", Id("a"), Id("b")),
				tstmt=BlockStmt([AssignStmt(Id("a"), IntegerLit(10))]),
				fstmt=BlockStmt([AssignStmt(Id("a"), IntegerLit(5))]),
			))
		)

		self.assertTrue(TestChecker.test(input, expect, 459))
	
	#def test_auto1(self):

	#	input = r"""

	#	"""

	def test_return1(self):
		
		input = r"""

		f : function float () {
			return 1;
		}

		b: function boolean () {
			return 2;
		}

		main : function void () {
			return;
		}
		"""

		expect = str(
			TypeMismatchInStatement(ReturnStmt(IntegerLit(2)))
		)

		self.assertTrue(TestChecker.test(input, expect, 458))

	def test_vardecl1(self):

		input = r"""
		a: integer = 1.1;

		main : function void () {}

		"""

		expect = str(
			TypeMismatchInVarDecl(VarDecl("a", IntegerType(), FloatLit(1.1)))
		)

		self.assertTrue(TestChecker.test(input, expect, 457))

	def test_operand1(self):

		input = r"""
		foo: function auto () {
	
		}
		bar: function integer () {
			return 1;
		}
		a: boolean = foo() == bar();

		main : function void () {
			a = false;
			b = true;
		}
		"""

		expect = str(
			Undeclared(Identifier(), "b")
		)

		self.assertTrue(TestChecker.test(input, expect, 455))

	def test_operand2(self):

		input = r"""
		main: function void () {
			a: integer = 12.2 % 2;
			}
		"""

		expect = str(
			TypeMismatchInExpression(BinExpr("%", FloatLit(12.2), IntegerLit(2)))	
		)

		self.assertTrue(TestChecker.test(input, expect, 454))

	def test_specialfunc1(self):
		
		input = r"""
		a: integer = 1;

		main : function void () {
			readInteger();
			printInteger(1);
			readFloat();
			writeFloat(1.1);
			readBoolean();
			printBoolean(true);
			readString();
			printString("abc");
			a = getInt();
		}

		"""

		expect = str(
			Undeclared(Function(), "getInt")
		)

		self.assertTrue(TestChecker.test(input, expect, 490))

	# TDDO type coercion / array literal as parameter / special funcs


	def test_specialfunc2(self):
		 
		input = r"""
		x: integer = 65;
		fact : function integer (n : integer ) {
			if (n == 0) return 1;
			else return n * fact (n - 1 ) ;
		}

		inc : function void (out n : integer , delta : integer ) {
			n = n + delta ;
		}
		
		main : function void () {
			delta : integer = fact ( 3 ) ;
			inc (x , delta ) ;
			printInteger(x) ;
			inc(y, delta) ;
		}

		"""

		expect = str(
			Undeclared(Identifier(), "y")
		)

		self.assertTrue(TestChecker.test(input, expect, 455))


	def test_void_callstmt(self):
		
		input = r"""
		a : integer = 1;
		foo: function auto () {
			return;
		}

		main : function void () {
			foo();
			a = foo();
		}
		"""

		expect = str(
			TypeMismatchInStatement(AssignStmt(Id("a"), FuncCall("foo", [])))
		)

		self.assertTrue(TestChecker.test(input, expect, 453))
	def test_inheritance1(self):

		input = r"""
		foo: function integer (inherit x: boolean) {
			return 1;
		}

		bar: function integer (y: boolean) inherit foo {
			super(y);
			return 1;
		}

		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 489))

	def test_inheritance2(self):

		input = r"""
	
		bar: function integer (y: boolean) inherit foo {
			preventDefault();
			return 2;
		}
		foo: function integer (a: boolean, inherit x: boolean) {
			return 1;
		}
		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 409))

	def test_inheritance3(self):

		input = r"""
		foo: function integer (inherit x: boolean) {
			return 1;
		}

		bar: function integer (a: boolean) inherit foo {
			return 2;
		}

		main : function void () {}
		"""

		expect = str(
			InvalidStatementInFunction("bar")
		)

		self.assertTrue(TestChecker.test(input, expect, 451))

	def test_inheritance4(self):

		input = r"""
		foo: function integer (inherit x: boolean) {
			return 1;
		}

		bar: function integer (x: boolean) inherit foo {
			super(x);
			return 2;
		}

		main : function void () {}
		"""

		expect = str(
			Invalid(Parameter(), "x")
		)

		self.assertTrue(TestChecker.test(input, expect, 409))

	def test_inheritance5(self):
		
		input = r"""
		foo: function integer (inherit x: boolean, y: boolean, inherit z: boolean) {
			return 1;
		}

		bar: function integer (x: boolean) inherit foo {
			super(true, false);
			return 2;
		}

		main : function void () {}
		"""

		expect = str(
			Invalid(Parameter(), "x")
		)

		self.assertTrue(TestChecker.test(input, expect, 408))

	def test_inheritance6(self):

		input = r"""
	
		bar: function integer (x: boolean) inherit foo {
			preventDefault();
			return 2;
		}
		foo: function integer (a: boolean, inherit x: boolean) {
			return 1;
		}
		//main : function void () {}
		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 452))

	def test_inheritance7(self):

		input = r"""
			bar: function integer (x: boolean) inherit foo {
		//	preventDefault();
			return 2;
		}
		foo: function integer () {
			return 1;
		}
	//	main : function void () {}
		
		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 453))

	def test_inheritance8(self):

		input = r"""
			bar: function integer (x: boolean) inherit foo {
			preventDefault();
			return 2;
		}
		foo: function integer () {
			return 1;
		}
	//	main : function void () {}
		
		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 453))	

	def test_inheritance9(self):

		input = r"""
	
		bar: function integer (x: boolean) inherit foo {
			preventDefault();
			return 2;
		}
		foo: function integer (inherit x: boolean) {
			return 1;
		}
		//main : function void () {}
		"""

		expect = str(
			NoEntryPoint()
		)

		self.assertTrue(TestChecker.test(input, expect, 452))


	def test_inheritance10(self):

		input = r"""
	
		bar: function integer (y: boolean) inherit foo {
			super();
			return 2;
		}
		foo: function integer (inherit x: boolean) {
			return 1;
		}
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(None)
		)

		self.assertTrue(TestChecker.test(input, expect, 452))

	def test_extra_forumbullshit1(self):

		input = r"""
		func: function integer() {

		a: integer = 12;

		return 3;

		a: float = 14;  

		}
		main: function void() {}
		"""

		expect = str(
			Redeclared(Variable(), "a")
		)

		self.assertTrue(TestChecker.test(input, expect, 489))

	def test_extra_forumbullshit2(self):

		input = r"""
		func: function integer() {

		a: integer = 12;

		return 3;

		a: float = 14; 
		}

		main: function void() {}
		"""

		expect = str(
			Redeclared(Variable(), "a")
		)

		self.assertTrue(TestChecker.test(input, expect, 489))

	def test_extra_forumbullshit3(self):

		input = r"""
			foo: function integer (inherit x: boolean, inherit y: boolean) {
			return 1;
		}
		bar : function integer (z: boolean) inherit foo {
			super(true);
		}
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(None)
		)

		self.assertTrue(TestChecker.test(input, expect, 489))
	
	def test_extra_forumbullshit4(self):
		"""https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9236"""

		input = r"""
		foo: function integer(inherit x: boolean) {
			return 1;
		}
		bar : function integer (z: boolean) inherit foo {
			super(true, z);
		}
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(Id("z"))
		)

		self.assertTrue(TestChecker.test(input, expect, 4800))

	def test_extra_forumbullshit5(self):
		"""https://e-learning.hcmut.edu.vn/mod/forum/discuss.php?d=9236"""

		input = r"""
		foo: function integer(inherit x: boolean, inherit y: boolean) {
			return 1;
		}
		bar : function integer (z: boolean) inherit foo {
			super(z, "wrong type");
		}
		main : function void () {}
		"""

		expect = str(
			TypeMismatchInExpression(StringLit("wrong type"))
		)

		self.assertTrue(TestChecker.test(input, expect, 489))