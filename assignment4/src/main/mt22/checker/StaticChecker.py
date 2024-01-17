# Truong Hong Hoa
# 1911185
from Visitor import Visitor
from StaticError import *
from AST import *

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
                if type(symbol.mtype) is MType:
                    symbol.mtype.rettype = typ 
                else:
                    symbol.mtype = typ
                return typ
    def findType(symbol_list, name):
        for symbol in symbol_list:
            if symbol.name == name:
                return symbol.mtype.rettype
            
    def inferParamAuto(symbol_list, list_func_param, funcname, paramname: str or int, typ):
        for symbol in symbol_list:
            if symbol.name == funcname and type(symbol.mtype) is MType:
                index = None
                for lst in list_func_param:
                    for i in range(len(lst)):
                        # lst = ['foo', 'b', 'c']
                        if isinstance(paramname, int):
                            symbol.mtype.partype[paramname] = typ
                            return 
                        if paramname in lst and lst[0] == funcname:
                            symbol.mtype.partype[lst.index(paramname)-1] = typ
                            return 
                       
class StaticChecker(Visitor):
    def __init__(self, ast):
        self.ast = ast
        self.has_entry_point = False
        self.is_in_loop = False
        self.is_return_type = None
        self.inherit = [None, 0, 0]    # ['hàm cha', vị trí của stmt, số tham số của hàm cha]
        self.scope = None           # tên hàm
        self.in_global = False
        self.name_list = ['readInteger', 'readFloat', 'readBoolean','readString','printInteger','printFloat','printBoolean', 'printString','preventDefault', 'super' ]
        self.is_func_body = False     # dành cho blockstmt quyết định envi
        self.param_name_list = []  ## list param name của hàm - dành cho auto
        
    def check(self):
        return self.visit(self.ast, [])

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
            Symbol("preventDefault", MType([], VoidType()))
        ]
        
        o = [global_env]

        for decl in ast.decls:
            if isinstance(decl, FuncDecl):
                if decl.name == "main" and type(decl.return_type) is VoidType and len(decl.params) == 0:
                    self.has_entry_point = True
                rettype = self.visit(decl.return_type, o)
                func = Symbol(decl.name, MType([],rettype), [])
                o[0].append(func)  
                self.scope = decl.name
                env = [[]] + o   
                self.param_name_list.append([decl.name])
                    
                for param in decl.params:
                    self.visit(param, env )
                    self.param_name_list[-1].append(param.name)

                ## thêm hàm super gọi đến function này
                super_func = Symbol('super', MType(func.mtype.partype,rettype), [], decl.name)
                o[0].append(super_func)  
                    
                self.scope = None
        
        for decl in ast.decls:
            if isinstance(decl, VarDecl):
                self.in_global = True
                if decl.name in self.name_list:
                    raise Redeclared(Variable(), decl.name)
        
                o = self.visit(decl, o)
                
            if isinstance(decl, FuncDecl):
                count = 0
                for x in o[0]:
                    if decl.name == x.name:
                        count += 1
                if count >= 2:    
                    raise Redeclared(Function(),decl.name)
                
                self.scope = decl.name
                env = [[]] + o

                if decl.inherit:
                    if decl.name == decl.inherit:
                        raise Undeclared(Function(), decl.name)
                    is_parentfunc_declared = False
                    for parentfunc in o[-1]:
                        if parentfunc.name == decl.inherit and type(parentfunc.mtype) is MType:
                            is_parentfunc_declared = True
                            inheritparams = parentfunc.inheritparams

                            ## check có câu lệnh đầu tiên preventDefault ko
                            if len(inheritparams) > 0: 
                                if len(decl.body.body) == 0 :
                                    raise InvalidStatementInFunction(decl.name)
                                elif type(decl.body.body[0]) is not CallStmt:
                                    raise InvalidStatementInFunction(decl.name)
                                elif type(decl.body.body[0]) is CallStmt:
                                    if not ((decl.body.body[0].name == 'preventDefault') and len(decl.body.body[0].args) == 0):
                                        # nếu là preventDefault thì không thêm inheritparams của hàm cha nữa 
                                        # ngược lại, thêm inherit params của hàm cha vào local scope của hàm con
                                        for parent_param in inheritparams:
                                            ## check invalid paramether : param ko thể trùng inherit param của hàm cha
                                            for child_param in decl.params :
                                                if child_param.name == parent_param.name:
                                                    raise Invalid(Parameter(), child_param.name)
                                            
                                            # thêm vào local env
                                            env[0].append(parent_param)
                                            #print(env[-1][-1].name)
                                            # thêm vào type params của hàm
                                            for func in o[-1]:
                                                if func.name == decl.name:
                                                    func.mtype.partype.append(parent_param.mtype)  
                                                    break                         
                                        
                            self.inherit = [parentfunc.name, 0, len(parentfunc.mtype.partype)] 
                            break
                        
                    if not is_parentfunc_declared:
                        raise Undeclared(Function(),decl.inherit)
                
                # thêm vào local list hiện tại
                for param in decl.params:
                    for var_local in env[0]:
                        if param.name in var_local.name: 
                            raise Redeclared(Parameter(), param.name)
                    env[0].append(Symbol(param.name, param.typ)) 
                 
                 
                #print(vars(env[-1][-1].mtype))
                self.is_func_body = True
                self.visit(decl, env)
                self.scope = None
                self.inherit = [None, 0, 0] 
            
            self.in_global = False
            self.name_list.append(decl.name)
        
        # print([vars(x.mtype) for x in o[0]])
        # print(vars(o[-1][-1].mtype))

        # check main function exist
        if not self.has_entry_point:
            raise NoEntryPoint()

        #print("in global :", [vars(x) for x in o[0]])
        return []
          
    def visitVarDecl(self, ast, o): 
        # name: str, typ: Type, init: Expr or None = None
        if not self.in_global:
            #print(ast.name, [vars(x )for x in o[0]])
            for decl in o[0]:
                if decl.name == ast.name:
                    raise Redeclared(Variable(), ast.name)
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
            dim = ast.typ.dimensions  # [3,2]
            typ_cell = ast.typ.typ           # integer
            if ast.init:
                init = self.visit(ast.init, o)  #(type, length)
                if type(init[0]) != type(typ_cell) or init[1] != dim[0]:
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
        # for param_decl in o[0]:
        #     if param_decl.name == ast.name:
        #         raise Redeclared(Parameter(), ast.name)
        
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
        # print(self.inherit[0] is not None and self.inherit[1] == 0 and self.inherit[2] != 0 and len(ast.body) == 0) 
        if self.inherit[0] is not None and self.inherit[1] == 0 and self.inherit[2] != 0 and len(ast.body) == 0:
            raise InvalidStatementInFunction(self.scope) 
        env = [[]] + o
        if self.is_func_body :
            env = o
            self.is_func_body = False
        
        for stmt in ast.body:
            self.visit(stmt, env)
            # if type(stmt) is BlockStmt:
            #     self.visit(stmt, [[]] + o)
            # else :
            #     #print('bbb',self.scope)
            #     self.visit(stmt, o)
            self.inherit[1] += 1
    # ở đây có check kiểu lhs và rhs
    # suy diễn kiểu cho function    
    def visitAssignStmt(self, ast, o): 
        # lhs: LHS, rhs: Expr
        # lhs là id, arraycell,
        lhs_type = self.visit(ast.lhs, o)
        rhs_type = self.visit(ast.rhs, o)

        if type(lhs_type) in [ArrayType, VoidType]:
            raise TypeMismatchInStatement(ast)
        
        # Trường hợp lhs auto trong param
        if type(lhs_type) is AutoType:
            lhs_type = FuncInfer.infer(o[0], ast.lhs.name, rhs_type)
            FuncInfer.inferParamAuto(o[-1],self.param_name_list, self.scope, ast.lhs.name, lhs_type)
            
        ## nếu rhs chỉ là một funccall ko có expr nào thêm thì cần suy diễn nó theo lhs
        if type(rhs_type) is AutoType:
            rhs_type = FuncInfer.infer(o[0], ast.rhs.name, lhs_type)
        
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
        if ast.fstmt:
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
            if type(return_type) is IntegerType and type(self.is_return_type) is FloatType:
                return
            if type(return_type) != type(self.is_return_type):
                raise TypeMismatchInStatement(ast)
    
    ## return type phải là VoidType
    ## callstmt chấp nhận tham số LHS = RHS => check như assign - undone
    def visitCallStmt(self, ast, o): 
        # name: str, args: List[Expr]
        # if self.inherit[0] and self.inherit[1] == 0:
        #     if not (ast.name in ['super', 'preventDefault']) :
        #         raise InvalidStatementInFunction(self.scope)
        #     return
        if ast.name in ['super', 'preventDefault']: # nếu là hàm super / preventdefault
            if self.inherit[0]:             # nếu có thừa kế
                if self.inherit[1] == 0:
                    if ast.name == 'super':
                        for superStmt in o[-1]:
                            if superStmt.super == self.inherit[0]:
                                # print(vars(superStmt.mtype))
                                # print(ast)      # CallStmt(super, IntegerLit(1), IntegerLit(1))
                                # check type super tới hàm cha
                                # superStmt : {'name': 'super', 'mtype': <StaticChecker.MType object at 0x000001E00B42B0D0>, 'inheritparams': [], 'super': 'parent'}
                                # superStmt.mtype:  {'partype': [<AST.IntegerType object at 0x00000185392C1E50>, <AST.StringType object at 0x00000185392C1F10>], 'rettype': <AST.VoidType object at 0x0000018538A1ADC0>}
                                """ 
                                len(arg) > len(param) ⇨ raise TypeMismatchInExpression với arg dư thừa đầu tiên
                                len(arg) < len(param) ⇨ raise TypeMismatchInExpression với đầu vào rỗng
                                len(arg) == len(param) nhưng có cặp arg & param không khớp kiểu ⇨ raise TypeMismatchInExpression với arg đầu tiên không khớp kiểu
                                """
                                length_args = len(ast.args)
                                length_superstmt = len(superStmt.mtype.partype)
                                #print("abc",ast.args[length_superstmt-length_args])
                                
                                if len(ast.args) < len(superStmt.mtype.partype):
                                    raise TypeMismatchInExpression(None)
                                if len(ast.args) > len(superStmt.mtype.partype):
                                    #print(ast.args[length_superstmt-length_args])
                                    raise TypeMismatchInExpression(ast.args[length_superstmt-length_args])
                                for i in range(len(ast.args)):
                                    if type(self.visit(ast.args[i], o)) != type(superStmt.mtype.partype[i]):
                                        raise TypeMismatchInExpression(ast.args[i])
                                    
                                ## check return type ??
                    
                else: 
                    raise InvalidStatementInFunction(self.scope)    
            else :
                raise InvalidStatementInFunction(self.scope)
            return
        for decl in o[-1]:
            if decl.name == ast.name and type(decl.mtype) is MType :
                callstmt_params_type = decl.mtype.partype
                # callstmt_return_type = decl.mtype.rettype
                
                if (len(ast.args)) != len(callstmt_params_type) :
                    raise TypeMismatchInStatement(ast) 

                for i in range(len(ast.args)):
                    itype = self.visit(ast.args[i], o)
                    ptype = callstmt_params_type[i]
                    if type(itype) != type(ptype):
                        if type(itype) is IntegerType and type(ptype) is FloatType:
                            continue
                        if type(ptype) is AutoType:
                            FuncInfer.inferParamAuto(o[-1],self.param_name_list,ast.name, i, itype)
                        else: raise TypeMismatchInStatement(ast) 
                return
        
        raise Undeclared(Function(),ast.name)

    def visitBinExpr(self, ast, o): 
        #  op: str, left: Expr, right: Expr
        ltype = self.visit(ast.left, o)
        rtype = self.visit(ast.right, o)
        if ast.op in ['+','-','*','/']:
            # suy diễn 
            if type(ltype) is AutoType and type(rtype) is AutoType:
               return AutoType()
            if type(ltype) is AutoType:
                ltype = FuncInfer.infer(o[-1],ast.left.name, rtype)
            if type(rtype) is AutoType:
                rtype = FuncInfer.infer(o[-1],ast.right.name, ltype)
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
            
            # if type(ltype) is IntegerType and type(rtype) is IntegerType:
            #     return BooleanType()
            # elif type(ltype) is FloatType and type(rtype) is FloatType:
            #     return BooleanType()
            if type(ltype) in [IntegerType, FloatType] and type(rtype) in [IntegerType, FloatType]:
                return BooleanType()
            raise TypeMismatchInExpression(ast)
            
    def visitUnExpr(self, ast, o): 
        # op: str, val: Expr
        valtyp = self.visit(ast.val, o)
        
        if ast.op == '-':
            if type(valtyp) is AutoType:
                valtyp = FuncInfer.infer(o[-1],ast.val.name, IntegerType())
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
                if ast.name == decl.name and type(decl.mtype) is not MType:
                    id_typ = decl.mtype
                    return id_typ
        if not id_typ :              
            raise Undeclared(Identifier(),ast.name)
        
    
    def visitArrayCell(self, ast, o): 
        # name: str, cell: List[Expr]
        # ArrayCell(arr, [IntegerLit(0)]
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
    """ 
    def findDim(a):     #{{1, 2}, {3, 4}, {5, 6}}
    print("ssss",a, type(a)== list)
    if not type(a) == list:
        return []
    return [len(a)] + findDim(a[0])
    
    """
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
        for decl in o[-1]:
            if decl.name == ast.name:
                if type(decl.mtype) is not MType:
                    raise Undeclared(Function(), ast.name)
                funccall_params_type = decl.mtype.partype
                funccall_return_type = decl.mtype.rettype
                if type(funccall_return_type) is VoidType:
                    raise TypeMismatchInExpression(ast)
                
                if (len(ast.args)) != len(funccall_params_type) :
                    raise TypeMismatchInExpression(ast) 
                for i in range(len(ast.args)):
                    itype = self.visit(ast.args[i], o)
                    ptype = funccall_params_type[i]
                    if type(itype) != type(ptype):
                        if type(itype) is IntegerType and type(ptype) is FloatType:
                            continue
                        if type(ptype) is AutoType:
                            FuncInfer.inferParamAuto(o[-1],self.param_name_list,ast.name, i, itype)
                        else: raise TypeMismatchInExpression(ast) 
                    
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

