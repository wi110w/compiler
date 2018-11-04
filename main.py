from lexer import Lexer
from tables import identifiers

string = '(* Let it be some comment *)\n' \
         'PROGRAM prog:( tell, well, sell );\n' \
         '(* Let * be * some * stars * *)'
lexer = Lexer()
lexer.parse_string(string)
print("Identifiers: ", identifiers)