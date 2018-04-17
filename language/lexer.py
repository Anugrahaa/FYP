#!/usr/bin/env python

import ply.lex as lex
import sys
import re


tokens = [
#Symbols
	'INCREMENT', 'DECREMENT', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUALS', 'MODULO', 'PERCENTAGE', 'LT', 'GT', 'LTE', 'GTE', 'COMMA',

	'OPENARRAY', 'CLOSEARRAY', 'OPENBLOCK', 'CLOSEBLOCK', 'OPENPARAM', 'CLOSEPARAM',
#literals
	'ID', 'STRINGLITERAL', 'INTEGERLITERAL', 'CHARLITERAL', 'DECIMALLITERAL', 'NEWLINE'

]

reserved = {
	'integer': 'INTEGER',
	'character': 'CHAR',
	'array':'ARRAY',
	'text': 'STRING',
	'decimal': 'DECIMAL',
	'$': 'VAR',
	'istrue': 'BOOLEAN',
	'and': 'AND',
	'or': 'OR',
	'is': 'EQUALCOMPARISON',
	'is not': 'NOTEQUALS',
	'invert': 'NOT',
	'True': 'TRUE',
	'False': 'FALSE',
	'calculate': 'FUNCTION',
	'if': 'IF',
	'else': 'ELSE',
	'while': 'WHILE',
	'break': 'BREAK',
	'return': 'RETURN',
	'begin': 'BEGIN',
	'end': 'END',
	'problem': 'PROBLEM',
	'set': 'STRUCTURE',
	'do': 'DO',
	'skip': 'CONTINUE',
	'of' : 'OF',
	'import': 'IMPORT'
}

tax = {
	'business': 'BUSINESS',
	'cash_ledger': 'CASH_LEDGER',
	'credit_ledger': 'CREDIT_LEDGER',
	'liability_ledger': 'LIABILITY_LEDGER',
	'invoice': 'INVOICE',
	'product': 'PRODUCT',
	'transaction': 'TRANSACTION',
	'utility': 'UTILITY'
}

tokens = tokens + reserved.values() + tax.values()

t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_PERCENTAGE = r'%%'
t_MODULO = r'%'

t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='

t_COMMA = r','
t_OPENARRAY = r'\['
t_CLOSEARRAY = r'\]'
t_OPENBLOCK = r'\{'
t_CLOSEBLOCK = r'\}'
t_OPENPARAM = r'\('
t_CLOSEPARAM = r'\)'

t_STRINGLITERAL = r'\"(.)*\"'
t_CHARLITERAL = r'\'(.)\''
t_INTEGERLITERAL = r'[0-9]+'
t_DECIMALLITERAL = r'[0-9]+\.[0-9]+'


def t_ignore_COMMENT(t):
	r'#(.)*(\n)?'

t_ignore = " \t"

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9]*'
	t.type = reserved.get(t.value, tax.get(t.value, 'ID'))
	return t

def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	return t

def t_error(t):
	line = t.lexer.lineno
	print("Character %s not recognized at line %d" % (t.value[0], line))
	t.lexer.skip(1)

# data = ''

lex.lex(reflags=re.IGNORECASE)
# lex.input(data)
# while True:
# 	tok = lex.token()
# 	if not tok: break
# 	print tok

data = open('sample.taxsol').read()
lex.input(data.lower())
while True:
	tok = lex.token()
	if not tok: break
	print tok