//1911185
//Truong Hong Hoa

grammar MT22;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

program			:	decls EOF ;
decls			: 	decl decls | decl ;
decl			: 	vardecl | funcdecl ;

vardecl 		:	(vardecl_assign | vardecl_no_assign) SEMI ;
vardecl_no_assign:  idlist COLON vartype  ;
idlist			: 	ID COMMA idlist | ID ;

vardecl_assign	:	varlist ; // a : auto = 1
varlist 		: 	ID COMMA varlist COMMA expr  | ID COLON vartype ASSIGN expr ;
vartype			: 	primtype|arraytype|AUTO ;

funcdecl		: 	funcprototype funcbody ;
funcprototype 	: 	ID COLON FUNCTION functype LB paramlist RB (INHERIT ID)? ;
functype 		: 	primtype| arraytype | VOID | AUTO ;
funcbody		: 	blockstmt  ;
paramlist		: 	paramlist COMMA paramdecl | paramdecl | ;
paramdecl		:	INHERIT? OUT? ID COLON vartype ;
stmts			:	stmts stmt_vardecl | stmt_vardecl ;
stmt_vardecl	: 	stmt | vardecl ;
stmt			: 	assignstmt
				|	ifstmt
				|	forstmt
				|	whilestmt
				|	dowhilestmt
				|	breakstmt
				| 	continuestmt
				|	returnstmt
				|	callstmt
				| 	blockstmt
				| 	specialfunc_c SEMI;

specialfunc_r	:	 ReadInteger			// function has return value  - funccall
				| 	 ReadFloat
				|	 ReadBoolean
				| 	 ReadString ;
specialfunc_c	:   PrintInteger LB expr RB	// it is stmt    callstmt
				|	PrintFloat LB expr RB
				|	PrintBoolean LB expr RB
				|	PrintString LB expr RB
				|	Super LB ( | exprlist) RB
				|	PreventDefault LB RB;
ReadInteger : 'readInteger()';
ReadFloat : 'readFloat()';
ReadBoolean: 'readBoolean()';
ReadString : 'readString()' ;
PrintInteger: 'printInteger';
PrintFloat: 'printFloat';
PrintBoolean: 'printBoolean';
PrintString : 'printString';
Super : 'super';
PreventDefault: 'preventDefault';

assignstmt		: 	lhs ASSIGN (expr|specialfunc_r) SEMI ;
lhs				:	ID | arrayidx ;						// scalarvar
ifstmt			:	IF LB expr RB stmt (ELSE stmt)? ;
forstmt			:	FOR LB init_for COMMA condexpr COMMA updateexpr RB stmt ;
init_for		: 	scalarvar ASSIGN intexpr ;
scalarvar		: ID;
intexpr			: ID | expr ;
condexpr		: expr;
updateexpr		: expr;
whilestmt		:	WHILE LB expr RB stmt ;
dowhilestmt		:	DO blockstmt WHILE LB expr RB SEMI;
breakstmt		:	BREAK SEMI ;
continuestmt	:	CONTINUE SEMI ;
returnstmt		:	RETURN (expr|) SEMI ;
callstmt		:	ID LB (exprlist|) RB SEMI ;		// func(a,b); do();
blockstmt		:	LP (stmts|) RP;


arraytype		: 	ARRAY LSB intlist RSB OF primtype ;		// array [2,3] of integer 	//kiểm tra số nguyên dương ở đây ?? chỉ có intlit được chấp nhận
arraylit		: 	LP (exprlist|) RP ;						// {a,1,2}	{{1,2},{2,3,4}} {}
arrayidx		: 	ID LSB exprlist RSB ;					// a[1, 0]

intlist			:	INTLIT COMMA intlist | INTLIT ; 
exprlist		:	expr COMMA exprlist | expr ;			//	a,b,c
expr			:	exp1 CONCATE exp1 | exp1 ;
exp1			: 	exp2 (EQ | NEQ | LT | GT | GEQ | LEQ) exp2 | exp2 ;
exp2			: 	exp2 (AND | OR) exp3 | exp3 ;
exp3			: 	exp3 (ADD | SUB) exp4 | exp4 ;
exp4			: 	exp4 (MUL | DIV | MOD) exp5 | exp5 ;
exp5			: 	NOT exp5 | exp6 ;
exp6			:	SUB exp6 | exp ;
//exp7			: 	exp7 LSB exprlist RSB | exp ; 			//a[1,2]

exp				: 	LB expr RB | ID | INTLIT | FLOATLIT | STRINGLIT | BOOLIT | arraylit | arrayidx | funccall | specialfunc_r;	
funccall		: 	ID LB (exprlist|) RB ; 					// a(a,b,c) a()
primtype		: 	INTEGER | FLOAT | STRING | BOOLEAN ;



//====================== Lexer =========================
//---------------------- seperators
LB:			'(';
RB:			')';
LP:			'{';
RP:			'}';
LSB:		'[';
RSB:		']';
DOT:		'.';
SEMI:		';';
COMMA:		',';
COLON:		':';


//---------------------- keyworks
ARRAY: 		'array';
AUTO: 		'auto';
BREAK:		'break';
BOOLEAN:	'boolean';
DO:			'do';
ELSE:		'else';
FLOAT:		'float';
FOR:		'for';
FUNCTION:	'function';
IF:			'if';
INTEGER:	'integer';
RETURN:		'return';
STRING:		'string';
VOID:		'void';
WHILE:		'while';
OUT:		'out';
CONTINUE:	'continue';
OF:			'of';
INHERIT:	'inherit';

//---------------------- operators
SUB:		'-';
ADD:		'+';
MUL:		'*';
DIV:		'/';
MOD:		'%';
CONCATE:	'::';
NOT:		'!';
AND:		'&&';
OR:			'||';
EQ:			'==';
NEQ:		'!=';
LT:			'<';
GT:			'>';
LEQ:		'<=';
GEQ:		'>=';
ASSIGN:		'=';

//---------------------- literals
INTLIT: '0'|[1-9]('_'?[0-9])*[0-9]* {self.text = self.text.replace("_", "")}; 
FLOATLIT: (INTPART DECPART | INTPART EXPPART | DECPART EXPPART | INTPART DECPART EXPPART ) {self.text = self.text.replace("_", "")};
fragment INTPART: '0'|[1-9]('_'?[0-9])*[0-9]* ; 
fragment DECPART: '.'[0-9]* ;
fragment EXPPART: [eE][+-]?[0-9]+ ;					
BOOLIT:	TRUE | FALSE ;
TRUE : 'true';
FALSE: 'false';

STRINGLIT: '"' STRINGCHAR* '"' {self.text = self.text[1:-1]}; //remove " "
fragment STRINGCHAR: ~["\\\n] | ESCAPESQUENCE ;
fragment ESCAPESQUENCE: '\\'[bfrnt"'\\];

ID:		[_a-zA-Z][_a-zA-Z0-9]*;

CMT: 		'//' ~[\n]*			-> skip;
BLOCKCMT:	'/*' (.)*? '*/'		-> skip;  // greedy
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

//---------------------- error 

ILLEGAL_ESCAPE: ( '"' ('\\'[bfrnt\\'] | ~[\n\r\\"])* ('\\'(~[bfrnt'\\]))) {self.text = self.text[1:]; raise IllegalEscape(self.text)};
UNCLOSED_STRING: ( '"' ('\'"' | '\\' [btnfr'\\] | ~[\r\t\n\\"] )* ) {self.text = self.text[1:]; raise UncloseString(self.text)};
ERROR_CHAR: . {raise ErrorToken(self.text)};
