from lexer import Lexer
from tables import identifiers

identifiers.clear()

string = 'PROGRAM HelloWorld;'
lexer = Lexer()
lexer.parse_string(string)