import ply.yacc as yacc
import sys
from lexer import tokens

def p_start(p):
	'start : PROBLEM ID newline program'
	print "heyy"

def p_program(p):
	'program : statement'
	pass
def p_newline(p):
	'''
	newline : NEWLINE newline
		   | NEWLINE
	'''
	pass

def p_statement(p):
	'''
	statement : block
			 | ifstatement 
			 | whilestatement 
			 | dowhilestatement
			 | CONTINUE newline
			 | BREAK newline
			 | returnstatement
			 | simplestatement
			 | empty
			 | newline
	'''
	pass
def p_block(p):
	'''
	block : statement
		 | statement block
	'''
	pass
def p_ifstatement(p):
	'''
	ifstatement : IF OPENPARAM expression CLOSEPARAM statement
			   | IF OPENPARAM expression CLOSEPARAM statement ELSE statement
	'''
	pass
def p_whilestatement(p):
	'''
	whilestatement : WHILE OPENPARAM expression CLOSEPARAM newline statement
	'''
	pass
def p_dowhilestatement(p):
	'dowhilestatement : DO statement WHILE OPENPARAM expression CLOSEPARAM newline'
	pass

def p_returnstatement(p):
	'returnstatement : RETURN expression newline'
	pass

def p_simplestatement(p):
	'''
	simplestatement : decs
					| expression
	'''
	pass

def p_decs(p):
	'''
	decs : dec newline decs
		| dec newline
	'''
	pass

def p_dec(p):
	'''
	dec : vardec
		| arraydec
		| functiondec
		| functiondefn
		| structuredec
	'''
	pass

def p_vardec(p):
	'vardec : type iddec'
	pass

def p_iddec(p):
	'''
	iddec : ID newline
		| ID COMMA iddec
		| ID EQUALS literal newline
		| ID EQUALS literal COMMA iddec
	'''

def p_arraydec(p):
	'''
	arraydec : ARRAY type ID newline
			| ARRAY type ID EQUALS OPENARRAY literalslist CLOSEARRAY newline
	'''
	pass

def p_functiondec(p):
	'''
	functiondec : FUNCTION ID OPENPARAM paramlist CLOSEPARAM
			   | FUNCTION ID OPENPARAM paramlist CLOSEPARAM newline
	'''
	pass

def p_paramlist(p):
	'''
	paramlist : type ID
				| type ID COMMA paramlist
				| empty
	'''
	pass

def p_functiondefn(p):
	'''
	functiondefn : functiondec newline BEGIN block returnstatement END newline
	'''
	pass

def p_structuredec(p):
	'structuredec : STRUCTURE ID newline BEGIN newline decs END newline'

def p_literal(p):
	'''
	literal : STRINGLITERAL
		   | INTEGERLITERAL
		   | CHARLITERAL
		   | DECIMALLITERAL
		   | TRUE
		   | FALSE
	'''
	pass

def p_literalslist(p):
	'''
	literalslist : literal
				| literal COMMA literalslist
	'''
	pass
def p_expression(p):
	'''
	expression : expression INCREMENT
			  | expression DECREMENT
			  | unaryop expression
			  | indexaccess
			  | memberaccess
			  | functioncall
			  | OPENPARAM expression CLOSEPARAM
			  | expression biop expression
			  | primaryexpression
			  | expression newline
	'''
	pass
def p_unaryop(p):
	'''
	unaryop : INCREMENT
		   | DECREMENT
		   | NOT
		   | PLUS
		   | MINUS
		   | PERCENTAGE
	'''
	pass
def p_biop(p):
	'''
	biop : MULTIPLY
		| DIVIDE
		| MODULO
		| PLUS
		| MINUS
		| AND
		| OR
		| LT
		| GT
		| LTE
		| GTE
		| EQUALCOMPARISON
		| NOTEQUALS
	'''
	pass
def p_indexaccess(p):
	'indexaccess : expression OPENARRAY expression CLOSEARRAY'
	pass
def p_memberaccess(p):
	'memberaccess : expression OF ID'
	pass
def p_functioncall(p):
	'functioncall : ID OPENPARAM callarguments CLOSEPARAM'
	pass
def p_callarguments(p):
	'''
	callarguments : ID
				 | literalslist
				 | ID COMMA callarguments
				 | literalslist COMMA callarguments
	'''
	pass

def p_primaryexpression(p):
	'''
	primaryexpression : literal
					 | ID
	'''
	pass

def p_type(p):
	'''
	type : INTEGER
		| CHAR
		| STRING
		| BOOLEAN
		| DECIMAL
	'''
	pass


def p_empty(p):
	'empty : '
	pass

def p_error(p):
    print "Syntax error in input!"

taxparser = yacc.yacc(debug=0)

def main():
	try:
		# data = open(sys.argv[1]).read()
		data = '''PROBLEM heyhey
array x '''
		data = data.lower()
		print data
	except IOError:
		print("exit")
		sys.exit()
	if not data:
		print("laa")
	result = taxparser.parse(data)
	# tok = ply.lex.tokens()
	print(result)

if __name__ == '__main__':
	main()
