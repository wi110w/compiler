from lexer import Lexer
from tables import identifiers


lexer = Lexer()
file = open('like-program.txt', 'r+')
samples = file.read()
lexer.parse_string(samples)
print("Identifiers: {0}".format(identifiers.keys()))
identifiers.clear()
file.close()