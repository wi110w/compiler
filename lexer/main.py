from lexer import Lexer
from tables import identifiers, constants
from lexer_task import LexerTask

# lexer = Lexer()
# file = open('like-program.txt', 'r')
# samples = file.read()
# lexer.parse_string(samples)
# print("Identifiers: {0}".format(identifiers.keys()))
# print("Numeric constants: {0}".format(constants.keys()))
# identifiers.clear()
# constants.clear()
# file.close()

lexer_task = LexerTask()
file = open('lexer-task.txt', 'r')
samples = file.read()
lexer_task.parse_string(samples)
print("Identifiers: {0}".format(identifiers.keys()))
identifiers.clear()
file.close()