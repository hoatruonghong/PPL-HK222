from Visitor import *
from AST import *
from StaticError import *

# Trương Hồng Hoa
# 1911185

"""
Check name and type

a : int = 1;
function a : int (b  : int) {
    a : float = 1.0;    
}
function main: void () {
}

"""
class StaticChecker(Visitor):
    
    #    def __init__(self, decls: List[Decl]):
    def visitProgram(self, ctx:Program, o): 
        
        o = []
        # for decl in ctx.decls:
        #     self.visit(decl, o)
        ## check whether main function exist or not
        is_main_func_defined = False
        for x in ctx.decls:
            if isinstance(x, FuncDecl) and x.name.name == 'main':
                is_main_func_defined = True
                break
                
        if not is_main_func_defined:
            raise NoEntryPoint()
    #    def __init__(self, name: str, typ: Type, init: Expr or None = None):    
    def visitVarDecl(self, ctx:VarDecl, o): 
        
        return 
    def visitFuncDecl(self, ctx:FuncDecl, o): 
        
        return
        
    def visitParamDecl(self, ctx:ParamDecl, o): pass
    
    def visitAssignStmt(self, ctx:AssignStmt, o): pass
    def visitBlockStmt(self, ctx:BlockStmt, o): pass
    def visitIfStmt(self, ctx:IfStmt, o): pass
    def visitForStmt(self, ctx:ForStmt, o): pass
    def visitWhileStmt(self, ctx:WhileStmt, o): pass
    def visitDoWhileStmt(self, ctx:DoWhileStmt, o): pass
    def visitBreakStmt(self, ctx:BreakStmt, o): 
        # is_in_loop = o[1]
        # if not is_in_loop:
        #     raise MustInLoop(ctx)
        pass
    def visitContinueStmt(self, ctx:ContinueStmt, o):
        pass
    def visitReturnStmt(self, ctx:ReturnStmt, o): pass
    def visitCallStmt(self, ctx:CallStmt, o): pass
    
    def visitFuncCall(self, ctx:FuncCall, o): pass
    def visitBinExpr(self, ctx:BinExpr, o): pass
    def visitUnExpr(self, ctx:UnExpr, o): pass
    def visitId(self, ctx:Id, o): pass
    def visitArrayCell(self, ctx:ArrayCell, o): pass
    
    def visitIntegerType(self, ctx:IntegerType, o): pass
    def visitFloatType(self, ctx:FloatType, o): pass
    def visitBooleanType(self, ctx:BooleanType, o): pass    
    def visitArrayType(self, ctx:ArrayType, o): 
        return ArrayType()
    def visitStringType(self, ctx:StringType, o): 
        return StringType()
    
    
    def visitArrayLit(self, ctx:ArrayLit, o): 
        return ArrayType()
    def visitIntegerLit(self, ctx:IntegerLit, o): 
        return IntegerType()
    def visitFloatLit(self, ctx:FloatLit, o): 
        return FloatType()
    def visitStringLit(self, ctx:StringLit, o): 
        return StringType()
    def visitBooleanLit(self, ctx:BooleanLit, o): 
        return BooleanType()
    
    
    
    
