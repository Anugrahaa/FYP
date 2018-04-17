import ply.yacc as yacc
import sys
from lexer import tokens
sys.path.insert(0, './Tax/')
from tax_functions import *
from prettify import prettify

symbol_table = []
status = []
complex_type = False
type_name = ""

def p_start(p):
	'start : PROBLEM ID newline imports newline program'
	p[0]= p[4]["value"]+"\ncontract " + p[2] + p[3]["value"] +"{ \n" + p[6]["value"] + "\n}\n"
	print "START:\n\n"+p[0]

def p_imports(p):
	'''imports : IMPORT import imports
				| IMPORT import'''

	p[0]={}
	p[0]["value"] = "import ./Helpers/"+p[2]["value"]+";\n"
	if len(p)==4:
		p[0]["value"]+=p[3]["value"]

def p_import(p):
	'''import : UTILITY
				| PRODUCT
				| INVOICE
				| BUSINESS
				| LIABILITY_LEDGER
				| CREDIT_LEDGER
				| CASH_LEDGER
				| TRANSACTION '''
	p[0]={}
	p[0]["value"] = p[1]+".sol"
	create_files(p[1])

def p_program(p):
	'program : block'
	p[0]={}
	p[0]["value"] = p[1]["value"]
	

def p_newline(p):
	'''
	newline : NEWLINE
	'''
	p[0] = {}
	p[0]["value"] = "\n"
	

def p_statement(p):
	'''
	statement : ifstatement 
			 | whilestatement 
			 | dowhilestatement
			 | continue newline
			 | break newline
			 | returnstatement
			 | simplestatement
			 | empty
			 | newline
	'''
	i=1
	p[0] = {}
	p[0]["value"]=""
	while i<len(p):
		p[0]["value"]+= p[i]["value"]+ "\n"
		i+=1

def p_block(p):
	'''
	block : statement
		 | statement block
	'''
	p[0]={}
	p[0]["value"] = p[1]["value"]
	if len(p)>2:
		p[0]["value"]+=p[2]["value"]

def p_ifstatement(p):
	'''
	ifstatement : if openparam expression closeparam newline begin block end
			   | if openparam expression closeparam newline begin block end else newline begin block end
	'''
	p[0]={}
	p[0]["value"] = "if("+p[3]["value"]+"){\n"+p[7]["value"]+"\n}\n"
	if len(p)==14:
		p[0]["value"]+= "else{\n"+p[12]["value"]+"\n}\n"
	

def p_whilestatement(p):
	'''
	whilestatement : while openparam expression closeparam newline begin block end
	'''
	p[0]={}
	p[0]["value"] = "while("+p[3]["value"]+"){\n"+p[7]["value"]+"\n}\n"
	

def p_dowhilestatement(p):
	'dowhilestatement : do newline begin block end newline while openparam expression closeparam'
	p[0]={}
	p[0]["value"] = "do{\n"+p[4]["value"]+"\n}while("+p[9]["value"]+");\n"
	

def p_returnstatement(p):
	'''returnstatement : empty
						| return expression newline'''
	p[0]={}
	if len(p)>2:
		p[0]["value"] = "return "+p[2]["value"]+";\n"
		p[0]["id"] = p[2]["value"]
	else:
		p[0]["value"] = ""
		p[0]["id"] = ""
	

def p_simplestatement(p):
	'''
	simplestatement : decs
					| expression
	'''
	p[0]={}
	p[0]["value"] = p[1]["value"]+";"
	

def p_decs(p):
	'''
	decs : dec decs
		| dec
	'''
	p[0]={}
	p[0]["value"] = p[1]["value"]
	if len(p)>2:
		p[0]["value"]+=p[2]["value"]
		

def p_dec(p):
	'''
	dec : vardec
		| arraydec
		| functiondefn
		| functiondec
		| structuredec
	'''
	p[0]={}
	p[0]["value"] = p[1]["value"]+"\n"
	

def p_vardec(p):
	'vardec : type iddec newline'
	p[0]={}
	p[0]["value"] = p[1]["value"]+" "+p[2]["value"]+";"
	
	global symbol_table, status, complex_type, type_name
	
	for i in xrange(1, len(p[2]["symtab"])):
		if not any(d.get("name",None) == p[2][i]["id"] for d in status):
			status.append({"name": p[2]["symtab"][i]["id"], "complex":"variable", "type":p[1]["value"], "dd":p[2]["symtab"][i]["dd"], "value": p[2]["symtab"][i]["value"]})
		else:
			raise "SyntaxError"


def p_iddec(p):
	'''
	iddec : id 
		| id comma iddec
		| id equals literal 
		| id equals literal comma iddec
	'''
	p[0]={}
	p[0]["value"] = ""
	p[0]["symtab"] = []
	i=1
	while i<len(p):
		p[0]["value"]+=p[i]["value"]+" "
		if p[i]["value"]!=',' and p[i]["value"]!='=' and p[i-1]["value"]!='=':
			if i==len(p)-1 or p[i+1]["value"]!='=':
				d = "nd"
				value = ""
			else:
				d = "d"
				value = p[i+2]["value"]
			p[0]["symtab"].append({"id": p[i]["value"], "dd": d, "value":value})

		i+=1
	

def p_arraydec(p):
	'''
	arraydec : array type id newline
			| array type id equals openarray literalslist closearray newline
	'''
	p[0] = {}
	p[0]["value"] = ""
	p[0]["value"] = p[2]["value"] +"[] " + p[3]["value"]
	if len(p)>5:
		p[0]["value"] += "=["+p[6]["value"]+"]"
		dd="d"
		value = "["+p[6]["value"]+"]"
	else:
		dd="nd"
		value = ""
	global status
	if not any(d.get("name",None) == p[3]["value"] for d in status):
		status.append({"name": p[3]["value"], "complex": "array", "type": p[2]["value"], "dd":dd, "value": value, "length": len(value.strip("[").strip("]").split(","))})
	p[0]["value"]+=";"
	

def p_functiondec(p):
	'''
	functiondec : function id openparam paramlist closeparam newline
	'''
	p[0]={}
	p[0]["value"] = "function "+p[2]["value"]+"("+p[4]["value"]+")\n"
	p[0]["id"] = p[2]["value"]
	if not any(d.get("name", None) == p[2]["value"] for d in status):
		status.append({"name": p[2]["value"], "complex": "function", "returntype":"", "dd":"nd"})
	

def p_paramlist(p):
	'''
	paramlist : type id
				| type id COMMA paramlist
				| empty
	'''
	p[0]={}	
	if len(p)==2:
		p[0]["value"] = p[1]["value"]
	else:
		p[0]["value"] = p[1]["value"]+" "+p[2]["value"]
		if len(p)>3:
			p[0]["value"]+=", "+p[4]["value"]


def p_functiondefn(p):
	'''
	functiondefn : functiondec begin block returnstatement end
	'''
	p[0]={}
	p[0]["value"] = p[1]["value"]+"{"+p[3]["value"]+p[4]["value"]+"\n}\n"
	insert_index = next((index for (index, d) in enumerate(status) if d["name"] == p[1]["id"]), None)
	if p[4]["id"]!="":
		return_index = next((index for (index, d) in enumerate(status) if d["name"] == p[4]["id"]), None)
		status[insert_index]["returntype"] = status[return_index]["type"]
	else:
		status[insert_index]["returntype"] = ""
	status[insert_index]["dd"] = "d"

	

def p_structuredec(p):
	'structuredec : structure id newline begin newline decs end newline'
	p[0]={}
	p[0]["value"]="struct "+p[2]["value"]+"{\n"+p[6]["value"]+"\n}\n"
	status.append({"name": p[2]["value"], "complex": "structure", "dd": "d"})

def p_literal(p):
	'''
	literal : STRINGLITERAL
		   | INTEGERLITERAL
		   | CHARLITERAL
		   | DECIMALLITERAL
		   | TRUE
		   | FALSE
	'''
	p[0] = {}
	p[0]["value"] = p[1]
	

def p_literalslist(p):
	'''
	literalslist : literal
				 | literal comma literalslist
	'''
	i=1
	p[0]={}
	p[0]["value"]=""
	while i<len(p):
		p[0]["value"] += p[i]["value"]
		i+=1

def p_expression(p):
	'''
	expression : unaryop expression
			  | indexaccess
			  | memberaccess
			  | functioncall
			  | openparam expression closeparam
			  | expression biop expression
			  | primaryexpression
			  | expression newline
			  | expression equals expression
	'''
	i=1
	p[0]={}
	p[0]["value"]=""
	while i<len(p):
		p[0]["value"]+=p[i]["value"]
		i+=1


def p_unaryop(p):
	'''
	unaryop : INCREMENT
		   | DECREMENT
		   | NOT
		   | PLUS
		   | MINUS
		   | PERCENTAGE
	'''
	p[0]={}
	if p[1]=="%%":
		p[0]["value"] = "*100"
	if p[1]=="invert":
		p[0]["value"] = "!"
	else:
		p[0]["value"]=p[1]
	

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
	p[0]={}
	if p[1]=="and":
		p[0]["value"]="&&"
	elif p[1]=="or":
		p[0]["value"]="||"
	elif p[1]=="is":
		p[0]["value"] = "=="
	elif p[1]=="is not":
		p[0]["value"] = "!="
	else:
		p[0]["value"]=p[1]

def p_equals(p):
	'equals : EQUALS'
	p[0]={}
	p[0]["value"] = p[1]

def p_indexaccess(p):
	'indexaccess : expression openarray expression closearray'
	p[0]={}
	p[0]["value"] = p[1]["value"]+"["+p[3]["value"]+"]"

def p_memberaccess(p):
	'memberaccess : expression of id'
	p[0]={}
	p[0]["value"] = p[3]["value"]+"."+p[1]["value"]

def p_functioncall(p):
	'functioncall : ID OPENPARAM callarguments CLOSEPARAM'
	if not any(d.get("name", None) == p[1]["value"] for d in status):
		raise SyntaxError
	else:
		index = next((index for (index, d) in enumerate(status) if d["name"] == p[1]["value"]), None)
		if status[index]["complex"]!="function":
			raise SyntaxError
	p[0]["value"] = p[1]["value"]+"("+p[3]["value"]+")"

def p_callarguments(p):
	'''
	callarguments : id
				 | literalslist
				 | id comma callarguments
				 | literalslist comma callarguments
	'''
	i=1
	p[0]={}
	p[0]["value"]=""
	while i<len(p):
		p[0]["value"]+=p[i]["value"]
		i+=1
	

def p_primaryexpression(p):
	'''
	primaryexpression : literal
					 | idknown
	'''
	p[0]={}
	p[0]["value"]=p[1]["value"]
	

def p_type(p):
	'''
	type : INTEGER
		| CHAR
		| STRING
		| BOOLEAN
		| DECIMAL
		| VAR
	'''
	p[0] = {}
	if p[1]=="integer":
		p[0]["value"] = "int"
	if p[1]=="character":
		p[0]["value"] = "char"
	if p[1]=="text":
		p[0]["value"] = "string"
	if p[1]=="istrue":
		p[0]["value"] = "bool"
	if p[1]=="decimal":
		p[0]["value"] = "fixed"
	if p[1]=="$":
		p[0]["value"] = "var"
	print p[0]["value"]

def p_idknown(p):
	'idknown : ID'
	p[0]={}
	p[0]["value"]=p[1]

def p_id(p):
	'id : ID'
	p[0]={}
	p[0]["value"]=p[1]

def p_comma(p):
	'comma : COMMA'
	p[0]={}
	p[0]["value"]=p[1]

def p_of(p):
	'of : OF'
	p[0]={}
	p[0]["value"]=p[1]

def p_openarray(p):
	'openarray : OPENARRAY'
	p[0]={}
	p[0]["value"]=p[1]

def p_closearray(p):
	'closearray : CLOSEARRAY'
	p[0]={}
	p[0]["value"]=p[1]

def p_openparam(p):
	'openparam : OPENPARAM'
	p[0]={}
	p[0]["value"]=p[1]

def p_closeparam(p):
	'closeparam : CLOSEPARAM'
	p[0]={}
	p[0]["value"]=p[1]

def p_begin(p):
	'begin : BEGIN'
	p[0]={}
	p[0]["value"]=p[1]

def p_end(p):
	'end : END'
	p[0]={}
	p[0]["value"]=p[1]

def p_structure(p):
	'structure : STRUCTURE'
	p[0]={}
	p[0]["value"]=p[1]

def p_function(p):
	'function : FUNCTION'
	p[0]={}
	p[0]["value"]=p[1]

def p_array(p):
	'array : ARRAY'
	p[0]={}
	p[0]["value"]=p[1]

def p_return(p):
	'return : RETURN'
	p[0]={}
	p[0]["value"]=p[1]

def p_do(p):
	'do : DO'
	p[0]={}
	p[0]["value"]=p[1]

def p_while(p):
	'while : WHILE'
	p[0]={}
	p[0]["value"]=p[1]

def p_if(p):
	'if : IF'
	p[0]={}
	p[0]["value"]=p[1]

def p_else(p):
	'else : ELSE'
	p[0]={}
	p[0]["value"]=p[1]

def p_break(p):
	'break : BREAK'
	p[0]={}
	p[0]["value"]=p[1]

def p_continue(p):
	'continue : CONTINUE'
	p[0]={}
	p[0]["value"]=p[1]

def p_empty(p):
	'empty : '
	pass

def p_error(token):
	if token is not None:
		print("Line "+str(token.lineno)+", illegal token: "+token.value)
	else:
	    print("Syntax error in input!")

taxparser = yacc.yacc(debug=0)
def main():
	global status
	try:
		input = open(sys.argv[1])
		data = input.read()
		data = data.lower()
		print(data)
	except IOError:
		print("exit")
		sys.exit()
	if not data:
		print("laa")
	result = taxparser.parse(data)
	print('--------------------------------------------\n'+result)

	print('--------------------------------------------\n'+str(status))
	input.close()

	i = 8
	filename = ""
	while result[i]!="\n":
		i+=1
	while result[i] == "\n":
		i+=1
	i+=9
	while result[i]!="\n":
		filename += result[i] 
		i+=1
	filename+=".sol"
	print filename
	output = open(filename, "w+")
	output.write("pragma solidity ^0.4.4;\n")
	output.write(result)
	output.close()
	prettify(filename)

if __name__ == '__main__':
	main()
