from Visitor import Visitor
from StaticError import *
from AST import *
## Truong Hong Hoa
## 1911185

class MType:
    def __init__(self, partype, rettype):
        self.partype = partype  # params type   kiểu list  
        self.rettype = rettype  # return type

class Symbol:
    def __init__(self, name, mtype, inheritparams = [] or None, parentname : str or None = None):
        self.name = name
        self.mtype = mtype
        self.inheritparams = inheritparams # [Symbol("a",IntegerType())]
        self.super = parentname             # Nếu chỗ này là hàm super thì có tên parentfunc
        
class FuncInfer:
    def infer(symbol_list, name, typ):
        for symbol in symbol_list:
            if symbol.name == name:
                symbol.mtype.rettype = typ 
                return typ
    def findType(symbol_list, name):
        for symbol in symbol_list:
            if symbol.name == name:
                return symbol.mtype.rettype
  
class StaticChecker(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.has_entry_point = False
        self.is_in_loop = False
        self.is_return_type = None
        self.scope = None
        self.func_list = [[]]
    
    def check(self):
        return self.visit(self.ast, [])

    """ 
    Tại global scope
    Lượt 1 : đưa name, returntyp, param của func   chưa check redeclared
    vào trong một cái list khác
    Lượt 2 : check vardecl, inherit của function
    """

    def visitProgram(self, ast, global_env): 
        # decls: List[Decl]
        #built-in function is in global scope
        global_env = [
            Symbol("readInteger", MType([], IntegerType())),
            Symbol("readFloat", MType([], FloatType())),
            Symbol("readBoolean", MType([], BooleanType())),
            Symbol("readString", MType([], StringType())),
            Symbol("printInteger", MType([IntegerType()], VoidType())),
            Symbol("printFloat", MType([FloatType()], VoidType())),
            Symbol("printBoolean", MType([BooleanType()], VoidType())),
            Symbol("printString", MType([StringType()], VoidType())),
        ]
        inherit_env = [
            Symbol("preventDefault", MType([], VoidType()))
        ]
        o = [inherit_env,global_env]
        
        #func_list = [[]]   # lụm các func prototype
        
        ## lần 1 lụm prototype của các hàm -> ko bắt lỗi gì kể cả redeclared
        ## prototype lưu vào func_list
        # func_list = [Symbol(name, MType([partype], rettype), inheritparams)]
        """Lần 1"""
        for decl in ast.decls:
            if isinstance(decl, FuncDecl):
                if decl.name == "main" and type(decl.return_type) is VoidType and len(decl.params) == 0:
                    self.has_entry_point = True
                rettype = self.visit(decl.return_type, o)
                func = Symbol(decl.name, MType([],rettype), [])
                self.func_list[0].append(func)  
                self.scope = decl.name
                env = [[]] + self.func_list                       
                for param in decl.params:
                    env = self.visit(param, env)
                self.scope = None
        
        #print([vars(x) for x in func_list[0]])
        #print("func list: ", [vars(x.mtype) for x in self.func_list[0]])

        """Lần 2"""
        for decl in ast.decls:
            if isinstance(decl, VarDecl):
                o = self.visit(decl, o)
            
            if isinstance(decl, FuncDecl):
                for x in o[0]:
                    if decl.name == x.name:
                        raise Redeclared(Function(),decl.name)
                
                rettype = self.visit(decl.return_type, o)
                func = Symbol(decl.name, MType([],rettype), [])
                o[0].append(func)  
                self.scope = decl.name
                env = [[]] + o

                if decl.inherit:
                    is_parentfunc_declared = False
                    for parentfunc in self.func_list[0]:
                        if parentfunc.name == decl.inherit:
                            is_parentfunc_declared = True
                            for x in o[-1]:
                                if x.name == parentfunc.name:
                                    parentfunc = x
                                    break
                            # thêm params vào local scope của hàm
                            inheritparams = parentfunc.inheritparams
                            for param in inheritparams:
                                env[0].append(param)
                                # thêm vào type params của hàm
                                env[-1][-1].mtype.partype.append(param.mtype)
                                
                            ## thêm hàm super ứng với parentfunc
                            env[-1].append(Symbol("super", MType([x.mtype for x in inheritparams],rettype),[],parentfunc.name))
                            break
                        
                    if not is_parentfunc_declared:
                        raise Undeclared(Function(),decl.inherit)
                
                for param in decl.params:
                    env = self.visit(param, env)
                
                self.visit(decl, env)
                self.scope = None
        
        
        # check main function exist
        if not self.has_entry_point:
            raise NoEntryPoint()

        #print("in global :", [vars(x) for x in o[0]])
        return []
          
    def visitVarDecl(self, ast, o): 
        # name: str, typ: Type, init: Expr or None = None
        for decl in o[0]:
            if decl.name == ast.name:
                raise Redeclared(Variable(),ast.name)
        if type(ast.typ) is AutoType:
            if not ast.init :
                raise Invalid(Variable(), ast.name)
            else:
                # suy diễn kiểu
                init_typ = self.visit(ast.init, o)               
                ast.typ = init_typ
        
        # kích thước array có bằng kích thước arraylit
        if type(ast.typ) is ArrayType:
            # ArrayType: dimensions: List[int], typ: AtomicType
            dim = ast.typ.dimensions  # [3]
            typ_cell = ast.typ.typ           # integer
            if ast.init:
                init = self.visit(ast.init, o)  #(type, length)
                if type(init[0]) != type(typ_cell):
                    raise TypeMismatchInVarDecl(ast)
            
        else: # atom type: int, float, bool, string
            if ast.init: # có init => kiểm tra về tương thích kiểu
                init_typ = self.visit(ast.init, o)
                if type(ast.typ) is FloatType and type(init_typ) is IntegerType:
                    if type(ast.init) is IntegerLit :
                        ast.init = FloatLit(float(ast.init.val))
                elif type(init_typ) is AutoType:
                    ## chỉ có trường hợp hàm còn kiểu auto
                    # for decl in o[-1]:
                    #     if decl.name == ast.init.name:
                    #         decl.mtype.rettype = ast.typ
                    init_typ = FuncInfer.infer(o[-1],ast.init.name, ast.typ)
                elif type(ast.typ) is not type(init_typ):
                    raise TypeMismatchInVarDecl(ast)
        
        #print("Vardecl: ",ast)        
        o[0].append((Symbol(ast.name, ast.typ)))   
        #print(vars(o[0][-1]))
        #print(o[0][-1].mtype)
        return o
        
    def visitParamDecl(self, ast, o): 
    # name: str, typ: Type, out: bool = False, inherit: bool = False
        for param_decl in o[0]:
            if param_decl.name == ast.name:
                raise Redeclared(Parameter(), ast.name)
        
        # thêm vào local list
        o[0].append(Symbol(ast.name, ast.typ))
        
        # thêm vào type hàm partypes -> rettype 
        for func in o[-1]:
            if func.name == self.scope:
                func.mtype.partype.append(ast.typ)
        
        # nếu là tham số có inherit của hàm cha thì thêm vào symbol của hàm (name, type, [])
        if ast.inherit:
            for func in o[-1]:
                if func.name == self.scope:
                    func.inheritparams.append(Symbol(ast.name, ast.typ))
               
        return o
        
    def visitFuncDecl(self, ast, o): 
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
        ## visit body : BlockStmt
        # env đang chứa [[local params], [global]]
        self.is_return_type = FuncInfer.findType(o[-1], ast.name)
        self.scope = ast.name
        self.visit(ast.body, o)   
        self.is_return_type = None
        self.scope = None
        return o

    def visitBlockStmt(self, ast, o): 
    #  body: List[Stmt or VarDecl]        
        for stmt in ast.body:
            if type(stmt) is BlockStmt:
                self.visit(stmt, [[]] + o)
            else :
                self.visit(stmt, o)

    # ở đây có check kiểu lhs và rhs
    # suy diễn kiểu cho function    
    def visitAssignStmt(self, ast, o): 
        # lhs: LHS, rhs: Expr
        # lhs là id, arraycell,
        lhs_type = self.visit(ast.lhs, o)
        rhs_type = self.visit(ast.rhs, o)
        
        if type(lhs_type) in [ArrayType, VoidType]:
            raise TypeMismatchInStatement(ast)
        
        ## nếu rhs chỉ là một funccall ko có expr nào thêm thì cần suy diễn nó theo lhs
        if type(rhs_type) is AutoType:
            rhs_type = FuncInfer.infer(o[-1], ast.rhs.name, lhs_type)
        
        if type(lhs_type) is FloatType and type(rhs_type) is IntegerType:
            return
        if type(lhs_type) != type(rhs_type):
            raise TypeMismatchInStatement(ast)
        
    def visitIfStmt(self, ast, o): 
        # cond: Expr, tstmt: Stmt, fstmt: Stmt or None = None
        cond_type = self.visit(ast.cond, o)
        if type(cond_type) is not BooleanType:
            raise TypeMismatchInStatement(ast)
        self.visit(ast.tstmt, o)
        self.visit(ast.fstmt, o)
        
    # for (scalar-variable = <init-expr>, <condition-expr>, <update-expr>)
    #     <statement>
    def visitForStmt(self, ast, o): 
        # init: AssignStmt, cond: Expr, upd: Expr, stmt: Stmt
        if type(self.visit(ast.init.lhs, o)) is not IntegerType:
            raise TypeMismatchInStatement(ast)
        if type(self.visit(ast.init.rhs, o)) is not IntegerType:
            raise TypeMismatchInStatement(ast)

        if type(self.visit(ast.cond, o)) is not BooleanType:
            raise TypeMismatchInStatement(ast)
        if type(self.visit(ast.upd, o)) is not IntegerType:
            raise TypeMismatchInStatement(ast)
        self.is_in_loop = True
        self.visit(ast.stmt, o)
        self.is_in_loop = False

    def visitWhileStmt(self, ast, o): 
        # cond: Expr, stmt: Stmt
        if type(self.visit(ast.cond, o)) is not BooleanType:
            raise TypeMismatchInStatement(ast)
        self.is_in_loop = True
        self.visit(ast.stmt, o)
        self.is_in_loop = False

    def visitDoWhileStmt(self, ast, o): 
        # cond: Expr, stmt: BlockStmt
        if type(self.visit(ast.cond, o)) is not BooleanType:
            raise TypeMismatchInStatement(ast)
        self.is_in_loop = True
        self.visit(ast.stmt, o)
        self.is_in_loop = False
        
    def visitBreakStmt(self, ast, o): 
        if not self.is_in_loop:
            raise MustInLoop(ast)
        
    def visitContinueStmt(self, ast, o): 
        if not self.is_in_loop:
            raise MustInLoop(ast)
        
    # Đối với câu lệnh trả về, biểu thức trả về có thể được coi là RHS 
    # của phép gán ẩn mà LHS là kiểu trả về.
    def visitReturnStmt(self, ast, o): 
        #  expr: Expr or None = None
        if ast.expr:
            return_type = self.visit(ast.expr, o)
            if type(self.is_return_type) is AutoType:
                self.is_return_type = FuncInfer.infer(o[-1], self.scope, return_type)
            if type(return_type) != type(self.is_return_type):
                raise TypeMismatchInStatement(ast)
    
    ## return type phải là VoidType
    ## callstmt chấp nhận tham số LHS = RHS => check như assign - undone
    def visitCallStmt(self, ast, o): 
        # name: str, args: List[Expr]
        for decl in o[-1]:
            if decl.name == ast.name:
                callstmt_params_type = decl.mtype.partype
                callstmt_return_type = decl.mtype.rettype
                if type(callstmt_return_type) is AutoType:
                    decl.mtype.rettype = VoidType()
                elif type(callstmt_return_type) is not VoidType:
                    raise TypeMismatchInStatement(ast)
                
                if (len(ast.args)) != len(callstmt_params_type) :
                    raise TypeMismatchInStatement(ast) 

                for i in range(len(ast.args)):
                    itype = self.visit(ast.args[i], o)
                    if type(itype) != type(callstmt_params_type[i]):
                        raise TypeMismatchInStatement(ast) 
                return
        
        for decl in self.func_list[-1]:
            if decl.name == ast.name:
                callstmt_params_type = decl.mtype.partype
                callstmt_return_type = decl.mtype.rettype
                if type(callstmt_return_type) is AutoType:
                    decl.mtype.rettype = VoidType()
                elif type(callstmt_return_type) is not VoidType:
                    raise TypeMismatchInStatement(ast)
                
                if (len(ast.args)) != len(callstmt_params_type) :
                    raise TypeMismatchInStatement(ast) 

                for i in range(len(ast.args)):
                    itype = self.visit(ast.args[i], o)
                    if type(itype) != type(callstmt_params_type[i]):
                        raise TypeMismatchInStatement(ast) 
                return
        raise Undeclared(Function(),ast.name)

    def visitBinExpr(self, ast, o): 
        #  op: str, left: Expr, right: Expr
        ltype = self.visit(ast.left, o)
        rtype = self.visit(ast.right, o)
        if ast.op in ['+','-','*','/']:
            # suy diễn nào kkk
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, rtype)
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, ltype)
            ## trường hợp cả hai đều là auto -> không thể suy diễn
            ## nhưng chưa có lỗi cho TH này
            if type(ltype) is IntegerType and type(rtype) is IntegerType:
                return IntegerType()
            if type(ltype) is FloatType or type(rtype) is FloatType:
                return FloatType()
            
            raise TypeMismatchInExpression(ast)
        
        if ast.op in ['%']:
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, IntegerType())
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, IntegerType())
            
            if not (type(ltype) is IntegerType and type(rtype) is IntegerType):
                raise TypeMismatchInExpression(ast)
            return IntegerType()
        
        if ast.op in ['&&', '||']:
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, BooleanType())
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, BooleanType())
            
            if type(ltype) is BooleanType and type(rtype) is BooleanType:
                return BooleanType()
            raise TypeMismatchInExpression(ast)
        
        if ast.op in ['::']:
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, StringType())
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, StringType())
            
            if type(ltype) is StringType and type(rtype) is StringType:
                return StringType()
            raise TypeMismatchInExpression(ast)
            
        if ast.op in ['==','!=']:
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, rtype)
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, ltype)
            
            if type(ltype) is IntegerType and type(rtype) is IntegerType:
                return BooleanType()
            elif type(ltype) is BooleanType and type(rtype) is BooleanType:
                return BooleanType()
            raise TypeMismatchInExpression(ast)
            
        if ast.op in ['>', '<', '<=','>=']:
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, rtype)
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, ltype)
            
            if type(ltype) is IntegerType and type(rtype) is IntegerType:
                return BooleanType()
            elif type(ltype) is FloatType and type(rtype) is FloatType:
                return BooleanType()
            raise TypeMismatchInExpression(ast)
            
    def visitUnExpr(self, ast, o): 
        # op: str, val: Expr
        valtyp = self.visit(ast.val, o)
        
        if ast.op == '-':
            if type(valtyp) is AutoType:
                valtyp = FuncInfer.infer(o[-1],ast.val.name, FloatType())
            if type(valtyp) in [IntegerType, FloatType]:
                return valtyp
            raise TypeMismatchInExpression(ast)
    
        if ast.op == '!':
            if type(valtyp) is AutoType:
                valtyp = FuncInfer.infer(o[-1],ast.val.name, BooleanType())
            if type(valtyp) is BooleanType:
                return BooleanType()
            raise TypeMismatchInExpression(ast)
       
    def visitId(self, ast, o): 
        # name: str        
        id_typ = None
        for env in o:
            for decl in env:
                if ast.name == decl.name:
                    id_typ = decl.mtype
                    break
        if not id_typ :              
            raise Undeclared(Identifier(),ast.name)
        return id_typ
    
    def visitArrayCell(self, ast, o): 
        # name: str, cell: List[Expr]
        # ArrayCell(arr, [IntegerLit(0)]
        #print(o[-1][-1].name)
        for env in o:
            for decl in env:
                if ast.name == decl.name: # có tồn tại biến
                    if type(decl.mtype) is ArrayType: # mang kiểu array
                        for idx in ast.cell:
                            idx_type = self.visit(idx, o)
                            if type(idx_type) is not IntegerType:
                                raise TypeMismatchInExpression(ast)
                        return decl.mtype.typ
                    else: raise TypeMismatchInExpression(ast) # tồn tại biến nhưng kiểu khác array
        raise Undeclared(Identifier(), ast.name)
 
    # kiểm tra type từng thành phần
    # trả về size của arraylit và type của arraycell
    def visitArrayLit(self, ast, o): 
        # explist: List[Expr]
        if len(ast.explist) == 0:
            return (None, 0)
        ele_type = self.visit(ast.explist[0],o)
        for exp in ast.explist:
            if type(ele_type) != type(self.visit(exp, o)) :
                raise IllegalArrayLiteral(ast)
        return (ele_type, len(ast.explist))
    
    """  
    check funccall:
    - có tên hàm tồn tại
    - có return type != None
    - thứ tự kiểu của params giống với định nghĩa hàm
    """
    def visitFuncCall(self, ast, o): 
        # name: str, args: List[Expr]
        env = o[-1]+self.func_list[-1]
        for decl in env:
            if decl.name == ast.name:
                funccall_params_type = decl.mtype.partype
                funccall_return_type = decl.mtype.rettype
                if type(funccall_return_type) is VoidType:
                    raise TypeMismatchInExpression(ast)
                
                if (len(ast.args)) != len(funccall_params_type) :
                    raise TypeMismatchInExpression(ast) 

                for i in range(len(ast.args)):
                    itype = self.visit(ast.args[i], o)
                    if type(itype) != type(funccall_params_type[i]):
                        raise TypeMismatchInExpression(ast) 
                return funccall_return_type
        raise Undeclared(Function(),ast.name)

    def visitIntegerLit(self, ast, o): 
        return IntegerType()
    def visitFloatLit(self, ast, o): 
        return FloatType()
    def visitStringLit(self, ast, o): 
        return StringType()
    def visitBooleanLit(self, ast, o): 
        return BooleanType()
    
    def visitIntegerType(self, ast, o): 
        return IntegerType()
    def visitFloatType(self, ast, o): 
        return FloatType()
    def visitBooleanType(self, ast, o): 
        return BooleanType()
    def visitStringType(self, ast, o): 
        return StringType()
    def visitArrayType(self, ast, o): 
        return ArrayType()
    def visitAutoType(self, ast, o): 
        return AutoType()
    def visitVoidType(self, ast, o): 
        return VoidType()

