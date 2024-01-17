from Emitter import Emitter
from functools import reduce

from Frame import Frame
from abc import ABC
from Visitor import *
from AST import *

## Truong Hong Hoa
## 1911185
class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype


class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return "Symbol(" + self.name + "," + str(self.mtype) + ")"


class CodeGenerator:
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("readInteger", MType(list(), IntegerType()), CName(self.libName)),
                Symbol("readFloat", MType(list(), FloatType()), CName(self.libName)),
                Symbol("readString", MType(list(), StringType()), CName(self.libName)),
                Symbol("readBoolean", MType(list(), BooleanType()), CName(self.libName)),
                
                Symbol("printInteger", MType([IntegerType()], VoidType()), CName(self.libName)),
                Symbol("printFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                Symbol("printString", MType([StringType()], VoidType()), CName(self.libName)),
                Symbol("printBoolean", MType([BooleanType()], VoidType()), CName(self.libName)),

                ]

    def gen(self, ast, path):
        # ast: AST
        # dir_: String
        gl = self.init()
        gc = CodeGenVisitor(ast, gl, path)
        gc.visit(ast, None)


class SubBody():
    def __init__(self, frame, sym, isGlobal = False):
        self.frame = frame
        self.sym = sym
        
        self.isGlobal = isGlobal

class Access():
    def __init__(self, frame, sym, isLeft, isFirst=False):
        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst


class Val(ABC):
    pass


class Index(Val):
    def __init__(self, value):
        self.value = value


class CName(Val):
    def __init__(self, value):
        self.value = value


class CodeGenVisitor(Visitor):
    def __init__(self, astTree, env, path):
        self.astTree = astTree
        self.env = env
        self.path = path
        self.className = 'MT22Class'
        self.emit = Emitter(self.path+'/'+self.className+'.j')
    
    def lookup(self, name, lst, func):
        for x in lst:
            if name == func(x):
                return x
        return None
    
    def visitProgram(self, ast, c):
        # ast : program
        # c : Any
        
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        
        staticDecl = self.env
        for x in ast.decls:
            if type(x) is FuncDecl:
                partype = [i.typ for i in x.params]
                staticDecl = [Symbol(x.name.lower(), MType(partype, x.return_type), CName(self.className))] + staticDecl
            else:
                newSym = self.visit(x, SubBody(None, None, isGlobal=True))
                staticDecl = [newSym] + staticDecl
        
        e = SubBody(None, staticDecl)
        [self.visit(x, e) for x in ast.decls if type(x) is FuncDecl]
        #print('aaaaaaaa',vars(self.emit))

        # # generate default constructor
        # self.genMETHOD(FuncDecl(Id("<init>"), list(), list(), list(), None), c, Frame("<init>", VoidType))
        # # class init - static field
        # self.genMETHOD(FuncDecl(Id("<clinit>"), list(), list(), list(), None), c, Frame("<clinit>", VoidType))
        
        self.emit.emitEPILOG()
        return c

    def visitVarDecl(self, ast, o): 
        #print(type(o), vars(o))
        if o.frame is None:
            code = self.emit.emitATTRIBUTE(ast.name, ast.typ, False, ast.init)
            self.emit.printout(code)
            return Symbol(ast.name, ast.typ, CName(self.className))
        else:    
            idx = o.frame.getNewIndex()
            code = self.emit.emitVAR(idx, ast.name,ast.typ, o.frame.getStartLabel(), o.frame.getEndLabel(), o.frame)
            self.emit.printout(code)
            return Symbol(ast.name, ast.typ, Index(idx))
            
    def visitParamDecl(self, ast, o): pass
    
    def visitFuncDecl(self, ast, o):
        #print('o:  ',o)
        frame = Frame(ast.name, ast.return_type)
        self.genMETHOD(ast, o.sym, frame)
        return Symbol(ast.name, MType([x.typ for x in ast.params], ast.return_type), CName(self.className))



    # def visitClassDecl(self, ast, c):
    #     self.className = ast.classname.name
    #     self.emit = Emitter(self.path+"/" + self.className + ".j")
    #     self.emit.printout(self.emit.emitPROLOG(
    #         self.className, "java.lang.Object"))
    #     [self.visit(ele, SubBody(None, self.env))
    #      for ele in ast.memlist if type(ele) == MethodDecl]
    #     # generate default constructor
    #     self.genMETHOD(MethodDecl(Instance(), Id("<init>"), list(
    #     ), None, Block([], [])), c, Frame("<init>", VoidType()))
    #     self.emit.emitEPILOG()
    #     return c

    def genMETHOD(self, consdecl, o, frame):
        #print('consdecl:  ',consdecl)
        isInit = consdecl.return_type is None
        isMain = consdecl.name == "main" and len(
            consdecl.params) == 0 and type(consdecl.return_type) is VoidType
        returnType = VoidType() if isInit else consdecl.return_type
        methodName = "<init>" if isInit else consdecl.name
        intype = [ArrayType(0, StringType())] if isMain else list(
            map(lambda x: x.typ, consdecl.params))
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(
            methodName, mtype, not isInit, frame))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(
                Id(self.className)), frame.getStartLabel(), frame.getEndLabel(), frame))
        elif isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType(
                0, StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            local = reduce(lambda env, ele: SubBody(
                frame, [self.visit(ele, env)]+env.sym), consdecl.params, SubBody(frame, []))
            glenv = local.sym+glenv

        body = consdecl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR(
                "this", ClassType(Id(self.className)), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body.body))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    ## ============ Visit Statements =============
    def handleCall(self, ast, frame, symbols, isStmt = False):
        # ast : FuncCall | CallStmt
        
        sym = self.lookup(ast.method.name.lower(), symbols, lambda x: x.name.lower())
        cname = sym.value.value
        ctype = sym.mtype
        paramTypes = ctype.partype
        
        paramCode = ""
        idx = 0
        for x in ast.param:
            pCode, pType = self.visit(x, Access(frame, symbols, False,True))
            if type(paramTypes[idx]) is FloatType and type(pType) is IntegerType:
                pCode = pCode + self.emit.emitI2F(frame)
            if type(paramTypes[idx]) is ArrayType:
                pass
                
            paramCode = paramCode + pCode
            idx += 1
            
        code = paramCode + self.emit.emitINVOKESTATIC(cname + '/' + sym.name, ctype, frame)
        if isStmt: 
            self.emit.printout(code)
        else: 
            return code, ctype.rettype
        

    def visitCallStmt(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = next(filter(lambda x: ast.name == x.name, nenv), None)
        cname = sym.value.value
        ctype = sym.mtype
        in_ = ("", list())
        for x in ast.args:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(
            cname + "/" + ast.name, ctype, frame))
    
    def visitAssignStmt(self, ast, o): 
        
        # visit LHS : id || arraycell
        expCode, expType = self.visit(ast.rhs, Access(o.frame, o.sym, False, True))
        lhsCode, lhsType = self.visit(ast.lhs, Access(o.frame, o.sym, True, True))
                


    def visitBlockStmt(self, ast, o): pass
    def visitIfStmt(self, ast, o): pass
    def visitForStmt(self, ast, o): pass
    def visitWhileStmt(self, ast, o): pass
    def visitDoWhileStmt(self, ast, o): pass
    def visitBreakStmt(self, ast, o): pass
    def visitContinueStmt(self, ast, o): pass
    def visitReturnStmt(self, ast, o): pass
    #def visitCallStmt(self, ast, o): pass

    ## ========== Visit Expression ===========
    ## Param:   o: Access(frame, sym, isLeft, isFirst)
    ## Return:  (code, type)

    def visitBinExpr(self, ast, o): 
        e1c, e1t = self.visit(ast.left, o)
        e2c, e2t = self.visit(ast.right, o)
        ## int - float
        if type(e1t) is type(e2t):
            rt = e1t
        elif type(e1t) is IntegerType and type(e2t) is FloatType:
            e1c = e1c + self.emit.emitI2F(o.frame)
            rt = e2t
        else:
            e2c = e2c + self.emit.emitI2F(o.frame)
            rt = e1t
            
        if ast.op in ['+', '-']:
            op = self.emit.emitADDOP(ast.op, rt, o.frame)
        elif ast.op in ['*']:
            op = self.emit.emitMULOP(ast.op, rt, o.frame)
        elif ast.op in ['/']:
            if type(e1t) is IntType and type(e2t) is IntType:
                e1c = e1c + self.emit.emitI2F(o.frame)
                e2c = e2c + self.emit.emitI2F(o.frame)
                rt = FloatType()
            op = self.emit.emitMULOP(ast.op, rt, o.frame)
        elif ast.op in ['%']:
            op = self.emit.emitMOD(o.frame)
        elif ast.op in ['&&']:
            op = self.emit.emitANDOP(o.frame)
        elif ast.op in ['||']:
            op = self.emit.emitOROP(o.frame)
        elif ast.op in ['::']:
            op = self.emit.emit
        elif ast.op in ['>', '<', '<=', '>=' ,'!=', '==']:
            op = self.emit.emitREOP(ast.op, rt, o.frame)
            
        
        return e1c + e2c + op , rt
        
    def visitUnExpr(self, ast, o): 
        ec, et = self.visit(ast.e, o)
        if ast.op in ['-']:
            return ec + self.emit.emitNEGOP(et, o.frame), et
        if ast.op in ['!']:
            return ec + self.emit.emitNOT(et, o.frame), et

        
    def visitId(self, ast, o): 
        sym = list(filter(lambda y: y.name == ast.name, o.sym))[0]
        if o.isLeft:
            if type(sym.value) is Index:
                code = self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, o.frame)
            else:
                code = self.emit.emitPUTSTATIC(sym.value.value+'.'+ sym.name, sym.mtype, o.frame)
                
        else:
            if type(sym.value) is Index:
                code = self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, o.frame)
            else:
                code = self.emit.emitGETSTATIC(sym.value.value+'.'+ sym.name, sym.mtype, o.frame)
            
        typ = sym.mtype
        return code, typ    
        
    def visitArrayCell(self, ast, o): 
        
        arrCode, arrType = self.visit(ast.name, Access(o.frame, o.sym, True, True))
        idxCode = reduce(lambda x, y: self.visit(x, Access(o.frame, o.sym, False, True)) + y, ast.cell)
        
        # aload(address index) -> iconst(access index) -> iaload
        if o.isLeft : 
            return arrCode + idxCode, self.emit.emitASTORE(arrType, o.frame), arrType
        else:
            return arrCode + idxCode + self.emit.emitALOAD(arrType, o.frame), arrType
                
    def visitIntegerLit(self, ast, o): 
        return self.emit.emitPUSHICONST(ast.val, o.frame), IntegerType()

    def visitFloatLit(self, ast, o): 
        return self.emit.emitPUSHFCONST(ast.val, o.frame), FloatType()
    
    def visitStringLit(self, ast, o): 
        return self.emit.emitPUSHICONST(ast.val, o.frame), StringType()
    
    def visitBooleanLit(self, ast, o): 
        return self.emit.emitPUSHICONST(ast.val, o.frame), BooleanType()
    
    def visitArrayLit(self, ast, o): pass
    def visitFuncCall(self, ast, o): 
        return self.handleCall(ast, o.frame, o.symbols, isStmt=False)
    

    