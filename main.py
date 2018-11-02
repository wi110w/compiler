from lexer import Lexer

string = 'PROGRAM HelloWorld;'
lexer = Lexer()
lexer.parse_string(string)