from signal_lexer.lexer import Lexer
from signal_lexer.tables import identifiers, constants
from signal_parser.parser import Parser

lexer_log = []
lexer = Lexer()
file = open('signal_lexer/tests.txt', 'r')
samples = file.read()
lexemes = lexer.parse_string(samples, lexer_log.append)
file.close()
# for log in lexer_log:
#     print(log)
# print("Identifiers: {0}".format(identifiers.keys()))

parser = Parser(lexemes)
parser.signal_program()
parser.print_tree()
# file = open('like-program.txt', 'r')
# samples = file.read()
# lexemes = signal_lexer.parse_string(samples)

# print("Numeric constants: {0}".format(constants.keys()))
# identifiers.clear()
# constants.clear()
# file.close()
