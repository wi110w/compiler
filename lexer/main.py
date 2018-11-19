from lexer import Lexer
from tables import identifiers, constants


lexer = Lexer()
file = open('like-program.txt', 'r')
samples = file.read()
lexer.parse_string(samples)
print("Identifiers: {0}".format(identifiers.keys()))
print("Numeric constants: {0}".format(constants.keys()))
identifiers.clear()
constants.clear()
file.close()
