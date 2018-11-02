keywords = {'PROGRAM', 'BEGIN', 'PROCEDURE', 'END', 'SIGNAL',
            'COMPLEX',  'INTEGER',  'FLOAT',  'BLOCKFLOAT',  'EXT'}
identifiers = set()
delimiters = {':',  ';',  ',',  ')'}
whitespaces = {'\n', ' ', '\r', '\t'}
#
# '''
# * Table of available symbols, where the first number is the ASCII code of
# * the symbol and the second is the category of the symbol.
# * Categories: 0 - whitespaces, 2 - identifiers, 3 - delimiters, 51 - comment delimiter.
# * Another symbols will be parsed by lexer as not-permitted and printed as an error.
# '''
# available_symbols = {
#     8: 0, 9: 0, 32: 0, 40: 51, 41: 3, 42: 3, 44: 3, 48: 2, 49: 2, 50: 2, 51: 2,
#     52: 2, 53: 2, 54: 2, 55: 2, 56: 2, 57: 2, 58: 3, 59: 3, 65: 2, 66: 2, 67: 2,
#     68: 2, 69: 2, 70: 2, 71: 2, 72: 2, 73: 2, 74: 2, 75: 2, 76: 2, 77: 2, 78: 2,
#     79: 2, 80: 2, 81: 2, 82: 2, 83: 2, 84: 2, 85: 2, 86: 2, 87: 2, 88: 2, 89: 2,
#     90: 2, 97: 2, 98: 2, 99: 2, 100: 2, 101: 2, 102: 2, 103: 2, 104: 2, 105: 2,
#     106: 2, 107: 2, 108: 2, 109: 2, 110: 2, 111: 2, 112: 2, 113: 2, 114: 2, 115: 2,
#     116: 2, 117: 2, 118: 2, 119: 2, 120: 2, 121: 2, 122: 2
# }