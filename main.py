from signal_lexer.lexer import Lexer
from signal_parser.parser import Parser

lexer_log = []
lexer = Lexer()
file = open('parser-tests/real-program.txt', 'r')
samples = file.read()
lexemes = lexer.parse_string(samples, lexer_log.append)
file.close()

parser = Parser(lexemes)
parser.signal_program()
parser.print_tree()
