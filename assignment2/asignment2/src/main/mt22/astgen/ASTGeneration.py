from MT22Visitor import MT22Visitor
from MT22Parser import MT22Parser
from AST import *
## Truong Hong Hoa
## 1911185
class ASTGeneration(MT22Visitor):
    # program			:	decls EOF ;
    def visitProgram(self, ctx:MT22Parser.ProgramContext):
        decls = self.visit(ctx.decls())
        return Program(decls)


    # decls			: 	decl decls | decl ;
    def visitDecls(self, ctx:MT22Parser.DeclsContext):
        if ctx.decls():
            return self.visit(ctx.decl()) + self.visit(ctx.decls())
        return self.visit(ctx.decl())


    # decl			: 	vardecl | funcdecl ;
    def visitDecl(self, ctx:MT22Parser.DeclContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        return self.visit(ctx.funcdecl())


    # vardecl 		:	(vardecl_assign | vardecl_no_assign) SEMI ;
    def visitVardecl(self, ctx:MT22Parser.VardeclContext):
        if ctx.vardecl_assign():
            return self.visit(ctx.vardecl_assign())
        return self.visit(ctx.vardecl_no_assign())
    # -> return list


    # vardecl_no_assign:  idlist COLON vartype  ;
    """
        abc,b,c : integer 
        [VarDecl(abc,IntegerType, None),
        VarDecl(b,IntegerType, None),
        VarDecl(c,IntegerType, None)]       
    
    """
    def visitVardecl_no_assign(self, ctx:MT22Parser.Vardecl_no_assignContext):
        # print("full ",ctx.idlist().getText())
        # idlist = ctx.idlist().getText()
        
        # intpart = idlist.partition(",")[0]
        # [print(id) for id in idlist]
        # [print(id) for id in ctx.idlist().getText()]
        idlist = self.visit(ctx.idlist())
        typ = self.visit(ctx.vartype())
        return list(map(lambda name: VarDecl(name, typ), idlist))

    # vardecl_assign	:	varlist ;
    """ antlr -> ngược thứ tự -> đảo list ??
        a,b,c : auto = 1,2,3
          b,c : auto = 1,2
            c : auto = 1
        solution: lấy danh sách id, expr rồi đảo một cái, mình đang đảo id list
        1. vardecl : a     3
        2. vardecl : a b   3 2
        3. vardecl : a b c 3 2 1
    """
    def visitVardecl_assign(self, ctx:MT22Parser.Vardecl_assignContext):  
        initlist = self.visit(ctx.varlist())
        typ = initlist[2]
        idlist = initlist[0]
        exprlist = initlist[1]
        
        return list(map(lambda name, expr: VarDecl(name, typ, expr), idlist, exprlist )) 
           
        
    # varlist 		: 	ID COMMA varlist COMMA expr  | ID COLON vartype ASSIGN expr ;
    def visitVarlist(self, ctx:MT22Parser.VarlistContext):  
        if ctx.varlist():
            initlist = self.visit(ctx.varlist())
            initlist[0].insert(0, ctx.ID().getText())
            initlist[1].append(self.visit(ctx.expr()))
            return initlist
        return [ctx.ID().getText()],[self.visit(ctx.expr())], self.visit(ctx.vartype())
           
                        
    # vartype			: 	primtype|arraytype|AUTO ;
    def visitVartype(self, ctx:MT22Parser.VartypeContext):
        if ctx.primtype():
            return self.visit(ctx.primtype())
        if ctx.arraytype():
            return self.visit(ctx.arraytype())
        if ctx.AUTO():
            return AutoType()


    # funcdecl		: 	funcprototype funcbody ;
    def visitFuncdecl(self, ctx:MT22Parser.FuncdeclContext):
        name, return_type, params, inherit = self.visit(ctx.funcprototype())
        body = self.visit(ctx.funcbody())
        return [FuncDecl(name, return_type, params, inherit, body )]


    # funcprototype 	: 	ID COLON FUNCTION functype LB paramlist RB (INHERIT ID)? ; 
    def visitFuncprototype(self, ctx:MT22Parser.FuncprototypeContext):
        name = ctx.ID(0).getText()
        return_type = self.visit(ctx.functype())
        params = self.visit(ctx.paramlist())
        inherit = None
        if ctx.INHERIT():
            inherit = ctx.ID(1).getText()
        return name, return_type, params, inherit 

    # functype 		: 	primtype| arraytype | VOID | AUTO ;
    def visitFunctype(self, ctx:MT22Parser.FunctypeContext):
        if ctx.primtype():
            return self.visit(ctx.primtype())
        if ctx.arraytype():
            return self.visit(ctx.arraytype())
        if ctx.VOID():
            return VoidType()
        if ctx.AUTO():
            return AutoType()


    # funcbody		: 	blockstmt  ;
    def visitFuncbody(self, ctx:MT22Parser.FuncbodyContext):
        return self.visit(ctx.blockstmt())


    # paramlist		: 	paramlist COMMA paramdecl | paramdecl | ;
        """
        function void(a,b,c: float)
        Param(a, float)
        Param(b, float)
        Param(c, float)
        """
    def visitParamlist(self, ctx:MT22Parser.ParamlistContext):
        if ctx.getChildCount() == 0:
            return []
        if ctx.COMMA():
            return self.visit(ctx.paramlist()) + self.visit(ctx.paramdecl())
        return self.visit(ctx.paramdecl())

    # paramdecl		:	INHERIT? OUT? ID COLON vartype ;
        """
        4 cases:                  num token
        - a : 1                     3 
        - out a : 1                 4
        - inherit a : 1             4
        - inherit out a : 1         5
        """
    def visitParamdecl(self, ctx:MT22Parser.ParamdeclContext):
        name = ctx.ID().getText()
        typ = self.visit(ctx.vartype())
        if ctx.getChildCount() == 3:
            return [ParamDecl(name, typ)]
        elif ctx.getChildCount() == 5 :
            return [ParamDecl(name, typ, True, True)]
        elif ctx.getChildCount() == 4: 
            if ctx.OUT():
                return [ParamDecl(name, typ, True, False)]
            else:
                return [ParamDecl(name, typ, False, True)]                            


    # stmts			:	stmts stmt_vardecl | stmt_vardecl ;
    def visitStmts(self, ctx:MT22Parser.StmtsContext):
        if ctx.stmts():
            return self.visit(ctx.stmts()) + self.visit(ctx.stmt_vardecl()) # trả list
        return self.visit(ctx.stmt_vardecl())   # trả list
# stmt_vardecl	: 	stmt | vardecl ;
    def visitStmt_vardecl(self, ctx:MT22Parser.Stmt_vardeclContext):
        if ctx.stmt():
            return [self.visit(ctx.stmt())]   # trả list 
        return self.visit(ctx.vardecl()) # trả về list


    # stmt			: 	assignstmt
	# 			|	ifstmt
	# 			|	forstmt
	# 			|	whilestmt
	# 			|	dowhilestmt
	# 			|	breakstmt
	# 			| 	continuestmt
	# 			|	returnstmt
	# 			|	callstmt
	# 			| 	blockstmt
	# 			| 	specialfunc_c SEMI;
 # trả về kiểu list gồm 1 statement
    def visitStmt(self, ctx:MT22Parser.StmtContext):
        stmt = None
        if ctx.assignstmt():
            stmt = self.visit(ctx.assignstmt())
        if ctx.ifstmt():
            stmt = self.visit(ctx.ifstmt())
        if ctx.forstmt():
            stmt = self.visit(ctx.forstmt())
        if ctx.whilestmt():
            stmt = self.visit(ctx.whilestmt())
        if ctx.dowhilestmt():
            stmt = self.visit(ctx.dowhilestmt())
        if ctx.breakstmt():
            stmt = self.visit(ctx.breakstmt())
        if ctx.continuestmt():
            stmt = self.visit(ctx.continuestmt())
        if ctx.returnstmt():
            stmt = self.visit(ctx.returnstmt())
        if ctx.callstmt():
            stmt = self.visit(ctx.callstmt())
        if ctx.blockstmt():
            stmt = self.visit(ctx.blockstmt())
        if ctx.specialfunc_c():
            stmt = self.visit(ctx.specialfunc_c())
        return stmt

    # specialfunc_r	:	 ReadInteger				// function has return value
	# 			| 	 ReadFloat
	# 			|	 ReadBoolean
	# 			| 	 ReadString ;
    def visitSpecialfunc_r(self, ctx:MT22Parser.Specialfunc_rContext):
        if ctx.ReadInteger():
            return FuncCall("readInteger", [])
        if ctx.ReadFloat():
            return FuncCall("readFloat", [])
        if ctx.ReadBoolean():
            return FuncCall("readBoolean", [])
        if ctx.ReadString():
            return FuncCall("readString", [])
        

    # specialfunc_c	:   PrintInteger LB expr RB	// function is called // it is stmt
	# 			|	PrintFloat LB expr RB
	# 			|	PrintBoolean LB expr RB
	# 			|	PrintString LB expr RB
	# 			|	Super LB exprlist RB
	# 			|	PreventDefault LB RB;
    #   printInteger(a);
    def visitSpecialfunc_c(self, ctx:MT22Parser.Specialfunc_cContext):
        if ctx.expr() :
            expr = [self.visit(ctx.expr())]
            return CallStmt(ctx.getChild(0).getText(), expr)
        if ctx.exprlist():
            exprlist = self.visit(ctx.exprlist())
            return CallStmt(ctx.Super().getText(), exprlist)
        return CallStmt(ctx.PreventDefault().getText(), [])


    # assignstmt		: 	lhs ASSIGN (expr|specialfunc_r) SEMI ;
    def visitAssignstmt(self, ctx:MT22Parser.AssignstmtContext):
        lhs = self.visit(ctx.lhs())
        if ctx.expr():
            rhs = self.visit(ctx.expr())
            return AssignStmt(lhs, rhs)
        if ctx.specialfunc_r():
            rhs = self.visit(ctx.specialfunc_r())
            return AssignStmt(lhs, rhs)


    # idlist			: 	ID COMMA idlist | ID ;
    def visitIdlist(self, ctx:MT22Parser.IdlistContext):
        if ctx.getChildCount() == 1 :
            return [ctx.ID().getText()]
        return [ctx.ID().getText()] + self.visit(ctx.idlist())


    # lhs				:	ID | arrayidx ;	
    def visitLhs(self, ctx:MT22Parser.LhsContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        return self.visit(ctx.arrayidx())


    # ifstmt			:	IF LB expr RB stmt (ELSE stmt)? ;
    def visitIfstmt(self, ctx:MT22Parser.IfstmtContext):
        cond = self.visit(ctx.expr())
        tstmt = self.visit(ctx.stmt(0))
        if ctx.ELSE():
            fstmt = self.visit(ctx.stmt(1))
            return IfStmt(cond, tstmt, fstmt)
        return IfStmt(cond, tstmt)        


    # forstmt			:	FOR LB init_for COMMA condexpr COMMA updateexpr RB stmt ;
    def visitForstmt(self, ctx:MT22Parser.ForstmtContext):
        init = self.visit(ctx.init_for())
        cond = self.visit(ctx.condexpr())
        upd = self.visit(ctx.updateexpr())
        stmt = self.visit(ctx.stmt())
        return ForStmt(init, cond, upd, stmt)

    # init_for		: 	scalarvar ASSIGN intexpr ;
    def visitInit_for(self, ctx:MT22Parser.Init_forContext):
        scalarvar = self.visit(ctx.scalarvar())
        intexpr = self.visit(ctx.intexpr())
        return AssignStmt(scalarvar, intexpr)
 
    # scalarvar		: ID;
    def visitScalarvar(self, ctx:MT22Parser.ScalarvarContext):
        return Id(ctx.ID().getText())     


    # intexpr			: ID | expr ;
    def visitIntexpr(self, ctx:MT22Parser.IntexprContext):
        if ctx.ID():
            return Id(ctx.ID().getText())            
        return self.visit(ctx.expr())


    # condexpr		: expr;
    def visitCondexpr(self, ctx:MT22Parser.CondexprContext):
        return self.visit(ctx.expr())


    # updateexpr		: expr;
    def visitUpdateexpr(self, ctx:MT22Parser.UpdateexprContext):
        return self.visit(ctx.expr())


    # whilestmt		:	WHILE LB expr RB stmt ;
    def visitWhilestmt(self, ctx:MT22Parser.WhilestmtContext):
        cond = self.visit(ctx.expr())
        stmt = self.visit(ctx.stmt())
        return WhileStmt(cond, stmt)

    # dowhilestmt		:	DO blockstmt WHILE LB expr RB SEMI;
    def visitDowhilestmt(self, ctx:MT22Parser.DowhilestmtContext):
        cond = self.visit(ctx.expr())
        stmt = self.visit(ctx.blockstmt())
        return DoWhileStmt(cond, stmt)

    # breakstmt		:	BREAK SEMI ;
    def visitBreakstmt(self, ctx:MT22Parser.BreakstmtContext):
        return BreakStmt()

    # continuestmt	:	CONTINUE SEMI ;
    def visitContinuestmt(self, ctx:MT22Parser.ContinuestmtContext):
        return ContinueStmt()


    # returnstmt		:	RETURN (expr|) SEMI ;
    def visitReturnstmt(self, ctx:MT22Parser.ReturnstmtContext):
        if ctx.expr():
            expr = self.visit(ctx.expr())
            return ReturnStmt(expr)
        return ReturnStmt()


    # callstmt		:	ID LB (exprlist|) RB SEMI ;             print(a,b,c)
    def visitCallstmt(self, ctx:MT22Parser.CallstmtContext):
        exprlist = []
        name = ctx.ID().getText()
        if ctx.exprlist():
            exprlist = self.visit(ctx.exprlist())
        return CallStmt(name, exprlist)


    # blockstmt		:	LP (stmts|) RP;
    def visitBlockstmt(self, ctx:MT22Parser.BlockstmtContext):
        body = []
        if ctx.getChildCount() != 2 :
            body = self.visit(ctx.stmts())
        return BlockStmt(body)


    # arraytype		: 	ARRAY LSB intlist RSB OF primtype ;
    def visitArraytype(self, ctx:MT22Parser.ArraytypeContext):
        intlist = self.visit(ctx.intlist())
        primtype = self.visit(ctx.primtype())
        return ArrayType(intlist, primtype)


    # arraylit		: 	LP (exprlist|) RP ;	
    def visitArraylit(self, ctx:MT22Parser.ArraylitContext):
        explist = []
        if ctx.exprlist():
            explist = self.visit(ctx.exprlist())
        return ArrayLit(explist)
    # ArrayLit([1,2,3,])


    # arrayidx		: 	ID LSB exprlist RSB ;
    def visitArrayidx(self, ctx:MT22Parser.ArrayidxContext):
        exprlist = self.visit(ctx.exprlist())
        id = ctx.ID().getText()
        return ArrayCell(id, exprlist)


    # intlist			:	INTLIT COMMA intlist | INTLIT ; 
    def visitIntlist(self, ctx:MT22Parser.IntlistContext):
        if ctx.getChildCount() == 1:
            return [int(ctx.INTLIT().getText())]
        return [int(ctx.INTLIT().getText())] + self.visit(ctx.intlist())


    # exprlist		:	expr COMMA exprlist | expr ; [expr 1, expr 2]
    def visitExprlist(self, ctx:MT22Parser.ExprlistContext):
        if ctx.COMMA():
            return [self.visit(ctx.expr())] + self.visit(ctx.exprlist())
        return [self.visit(ctx.expr())]       


    # expr			:	exp1 CONCATE exp1 | exp1 ;
    def visitExpr(self, ctx:MT22Parser.ExprContext):
        if ctx.CONCATE():
            left = self.visit(ctx.exp1(0))
            right = self.visit(ctx.exp1(1))
            return BinExpr("::", left, right)
        return self.visit(ctx.exp1(0))


    # exp1			: 	exp2 (EQ | NEQ | LT | GT | GEQ | LEQ) exp2 | exp2 ;
    def visitExp1(self, ctx:MT22Parser.Exp1Context):
        if ctx.getChildCount() == 1 :
            return self.visit(ctx.exp2(0))
        left = self.visit(ctx.exp2(0))
        right = self.visit(ctx.exp2(1))
        if ctx.EQ():
            return BinExpr("==", left, right)
        if ctx.NEQ():
            return BinExpr("!=", left, right)
        if ctx.LT():
            return BinExpr("<", left, right)
        if ctx.GT():
            return BinExpr(">", left, right)
        if ctx.GEQ():
            return BinExpr(">=", left, right)
        if ctx.LEQ():
            return BinExpr("<=", left, right)
        
    # exp2			: 	exp2 (AND | OR) exp3 | exp3 ;
    def visitExp2(self, ctx:MT22Parser.Exp2Context):
        if ctx.exp2():
            exp2 = self.visit(ctx.exp2())
            exp3 = self.visit(ctx.exp3())
            if ctx.AND():
                return BinExpr("&&", exp2, exp3)
            if ctx.OR():
                return BinExpr("||", exp2, exp3) 
        return self.visit(ctx.exp3())


    # exp3			: 	exp3 (ADD | SUB) exp4 | exp4 ;
    def visitExp3(self, ctx:MT22Parser.Exp3Context):
        if ctx.exp3():
            exp3 = self.visit(ctx.exp3())
            exp4 = self.visit(ctx.exp4())
            if ctx.ADD():
                return BinExpr("+", exp3, exp4)
            if ctx.SUB():
                return BinExpr("-", exp3, exp4) 
        return self.visit(ctx.exp4())


    # exp4			: 	exp4 (MUL | DIV | MOD) exp5 | exp5 ;
    def visitExp4(self, ctx:MT22Parser.Exp4Context):
        if ctx.exp4():
            exp4 = self.visit(ctx.exp4())
            exp5 = self.visit(ctx.exp5())
            if ctx.MUL():
                return BinExpr("*", exp4, exp5)
            if ctx.DIV():
                return BinExpr("/", exp4, exp5) 
            if ctx.MOD():
                return BinExpr("%", exp4, exp5)
        return self.visit(ctx.exp5())


    # exp5			: 	NOT exp5 | exp6 ;
    def visitExp5(self, ctx:MT22Parser.Exp5Context):
        if ctx.exp5():
            exp5 = self.visit(ctx.exp5())
            return UnExpr("!",exp5)
        return self.visit(ctx.exp6())

    # exp6			:	SUB exp6 | exp ;
    def visitExp6(self, ctx:MT22Parser.Exp6Context):
        if ctx.exp6():
            exp6 = self.visit(ctx.exp6())
            return UnExpr("-",exp6)
        return self.visit(ctx.exp())

    # exp	: 	LB expr RB | ID | INTLIT | FLOATLIT | STRINGLIT | BOOLIT | arraylit |  arrayidx | funccall | specialfunc_r;	
    def visitExp(self, ctx:MT22Parser.ExpContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INTLIT():
            return IntegerLit(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLit(float("0"+ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLit(ctx.STRINGLIT().getText())
        elif ctx.BOOLIT():
            return BooleanLit(ctx.BOOLIT().getText()=='true')
        elif ctx.arraylit():
            return self.visit(ctx.arraylit())
        elif ctx.arrayidx():
            return self.visit(ctx.arrayidx())
        elif ctx.funccall():
            return self.visit(ctx.funccall())
        elif ctx.specialfunc_r():
            return self.visit(ctx.specialfunc_r())

    # funccall		: 	ID LB (exprlist|) RB ; 			
    def visitFunccall(self, ctx:MT22Parser.FunccallContext):
        id = ctx.ID().getText()
        if ctx.exprlist():
            exprlist = self.visit(ctx.exprlist())
            return FuncCall(id, exprlist)
        else:
            return FuncCall(id, [])

    # primtype		: 	INTEGER | FLOAT | STRING | BOOLEAN ;
    def visitPrimtype(self, ctx:MT22Parser.PrimtypeContext):
        if ctx.INTEGER(): 
            return IntegerType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.BOOLEAN():
            return BooleanType()
        else:
            return StringType()
        
