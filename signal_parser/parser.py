from signal_lexer.tables import *

BEGIN_ATTRIBUTES_CODE = 405
END_ATTRIBUTES_CODE = 410
ERROR = -1
OK = 0
EMPTY = 1


class Parser:
    def __init__(self, lexemes):
        self.shift = 0
        self.lexemes = lexemes
        self.tree = ''

    def signal_program(self):
        self.append_to_tree('<signal-program>')
        self.program()

    def program(self):
        self.shift += 1
        lexeme = self.advance_lexeme()
        if lexeme.code != keywords["PROGRAM"]:
            self.add_error(lexeme.line, lexeme.column, 'keyword', 'PROGRAM', lexeme.value)
            return
        self.append_to_tree('<program>')
        self.add_lexeme(lexeme.code, lexeme.value)
        code = self.procedure_identifier()
        if code is ERROR:
            return
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[';']:
            self.add_error(lexeme.line, lexeme.column, 'delimiter', ';', lexeme.value)
            return
        self.add_lexeme(lexeme.code, lexeme.value)
        code = self.block()
        if code is ERROR:
            return
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[';']:
            self.add_error(lexeme.line, lexeme.column, 'delimiter', ';', lexeme.value)
            return
        self.add_lexeme(lexeme.code, lexeme.value)
        self.shift -= 1

    def procedure_identifier(self):
        self.shift += 1
        lexeme = self.advance_lexeme()
        if lexeme.code not in identifiers.values():
            self.add_error(lexeme.line, lexeme.column, 'identifier', actual=lexeme.value)
            return ERROR
        self.append_to_tree('<procedure-identifier>')
        self.identifier(lexeme.code, lexeme.value)
        self.shift -= 1
        return OK

    def block(self):
        self.shift += 1
        self.append_to_tree('<block>')
        code = self.declarations()
        if code is ERROR:
            return ERROR
        lexeme = self.advance_lexeme()
        if lexeme.code != keywords['BEGIN']:
            self.add_error(lexeme.line, lexeme.column, 'keyword', 'BEGIN', lexeme.value)
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        self.statements_list()
        lexeme = self.advance_lexeme()
        if lexeme.code != keywords['END']:
            self.add_error(lexeme.line, lexeme.column, 'keyword', 'END', lexeme.value)
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        self.shift -= 1

    def declarations(self):
        self.shift += 1
        self.append_to_tree('<declarations>')
        code = self.procedure_declarations()
        self.shift -= 1
        if code is ERROR:
            return ERROR

    def statements_list(self):
        self.shift += 1
        self.append_to_tree('<empty>')
        self.shift -= 1

    def procedure_declarations(self):
        self.shift += 1
        self.append_to_tree('<procedure-declarations>')
        code = self.procedure()
        if code is OK:
            code = self.procedure_declarations()
        self.shift -= 1
        return code

    def procedure(self):
        self.shift += 1
        lexeme = self.current_lexeme
        if lexeme.code != keywords['PROCEDURE']:
            self.append_to_tree('<empty>')
            self.shift -= 1
            return EMPTY
        lexeme = self.advance_lexeme()
        self.append_to_tree('<procedure>')
        self.add_lexeme(lexeme.code, lexeme.value)
        code = self.procedure_identifier()
        if code is ERROR:
            self.shift -= 1
            return ERROR
        code = self.parameters_list()
        if code is ERROR:
            self.shift -= 1
            return ERROR
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[';']:
            self.add_error(lexeme.line, lexeme.column, 'delimiter', ';', lexeme.value)
            self.shift -= 1
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        self.shift -= 1
        return OK

    def parameters_list(self):
        self.shift += 1
        lexeme = self.current_lexeme
        if lexeme.code != delimiters['(']:
            self.append_to_tree('<empty>')
            self.shift -= 1
            return EMPTY
        lexeme = self.advance_lexeme()
        self.append_to_tree('<parameters-list>')
        self.add_lexeme(lexeme.code, lexeme.value)
        code = self.declarations_list()
        if code is ERROR:
            self.shift -= 1
            return ERROR
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[')']:
            self.add_error(lexeme.line, lexeme.column, 'delimiter', ')', lexeme.value)
            self.shift -= 1
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        self.shift -= 1
        return OK

    def declarations_list(self):
        self.shift += 1
        self.append_to_tree('<declarations-list>')
        code = self.declaration()
        if code is OK:
            code = self.declarations_list()
        self.shift -= 1
        return code

    def declaration(self):
        self.shift += 1
        self.append_to_tree('<declaration>')
        code = self.variable_identifier()
        if code is EMPTY:
            self.append_to_tree('<empty>')
            self.shift -= 1
            return EMPTY
        code = self.identifiers_list()
        if code is ERROR:
            self.shift -= 1
            return ERROR
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[':']:
            self.add_error(lexeme.line, lexeme.column, 'delimiter', ':', lexeme.value)
            self.shift -= 1
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        lexeme = self.advance_lexeme()
        if BEGIN_ATTRIBUTES_CODE <= lexeme.code <= END_ATTRIBUTES_CODE or lexeme.code == delimiters['(']:
            self.attribute()
        else:
            self.add_error(lexeme.line, lexeme.column, 'attribute',
                           'SIGNAL, COMPLEX, INTEGER, FLOAT, BLOCKFLOAT, EXT, (<digit>:<digit>)', lexeme.value)
            self.shift -= 1
            return ERROR
        self.attributes_list()
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[';']:
            self.add_error(lexeme.line, lexeme.column, 'delimiter', ';', lexeme.value)
            self.shift -= 1
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        self.shift -= 1
        return OK

    def variable_identifier(self):
        self.shift += 1
        lexeme = self.current_lexeme
        if lexeme.code not in identifiers.values():
            self.shift -= 1
            return EMPTY
        lexeme = self.advance_lexeme()
        self.append_to_tree('<variable-identifier>')
        self.identifier(lexeme.code, lexeme.value)
        self.shift -= 1
        return OK

    def identifiers_list(self):
        self.shift += 1
        lexeme = self.current_lexeme
        if lexeme.code != delimiters[',']:
            self.append_to_tree('<empty>')
            self.shift -= 1
            return EMPTY
        lexeme = self.advance_lexeme()
        self.add_lexeme(lexeme.code, lexeme.value)
        code = self.variable_identifier()
        if code is OK:
            code = self.identifiers_list()
        self.shift -= 1
        return code

    def attributes_list(self):
        self.shift += 1
        lexeme = self.current_lexeme
        if BEGIN_ATTRIBUTES_CODE <= lexeme.code <= END_ATTRIBUTES_CODE or lexeme.code == delimiters['(']:
            self.append_to_tree('<attributes-list>')
            self.attribute()
            self.attributes_list()
        self.shift -= 1

    def attribute(self):
        self.shift += 1
        lexeme = self.advance_lexeme()
        self.append_to_tree('<attribute>')
        self.add_lexeme(lexeme.code, lexeme.value)
        lexeme = self.advance_lexeme()
        if lexeme.code not in constants.values():
            self.add_error(lexeme.line, lexeme.column, 'attribute',
                           'SIGNAL, COMPLEX, INTEGER, FLOAT, BLOCKFLOAT, EXT, (<digit>:<digit>)', lexeme.value)
            self.shift -= 1
            return ERROR
        self.digit(lexeme.code, lexeme.value)
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[':']:
            self.add_error(lexeme.line, lexeme.column, 'attribute',
                           'SIGNAL, COMPLEX, INTEGER, FLOAT, BLOCKFLOAT, EXT, (<digit>:<digit>)', lexeme.value)
            self.shift -= 1
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        lexeme = self.advance_lexeme()
        if lexeme.code not in constants.values():
            self.add_error(lexeme.line, lexeme.column, 'attribute',
                           'SIGNAL, COMPLEX, INTEGER, FLOAT, BLOCKFLOAT, EXT, (<digit>:<digit>)', lexeme.value)
            self.shift -= 1
            return ERROR
        self.digit(lexeme.code, lexeme.value)
        lexeme = self.advance_lexeme()
        if lexeme.code != delimiters[')']:
            self.add_error(lexeme.line, lexeme.column, 'attribute',
                           'SIGNAL, COMPLEX, INTEGER, FLOAT, BLOCKFLOAT, EXT, (<digit>:<digit>)', lexeme.value)
            self.shift -= 1
            return ERROR
        self.add_lexeme(lexeme.code, lexeme.value)
        self.shift -= 1

    def identifier(self, code, value):
        self.shift += 1
        self.append_to_tree('<identifier>')
        self.add_lexeme(code, value)
        self.shift -= 1

    def digit(self, code, value):
        self.shift += 1
        self.append_to_tree('<digit>')
        self.add_lexeme(code, value)
        self.shift -= 1

    def add_lexeme(self, code, value):
        self.shift += 1
        self.append_to_tree('{0} {1}'.format(code, value))
        self.shift -= 1

    def add_error(self, line, column, lexeme_type, expected='', actual=''):
        if lexeme_type == 'keyword':
            self.tree += "\nParser Error: Expected keyword '{}', got '{}' " \
                         "at line {}, column {}".format(expected, actual, line, column)
            return
        if lexeme_type == 'identifier':
            self.tree += "\nParser Error: Expected identifier, got '{}' " \
                         "at line {}, column {}".format(actual, line, column)
            return
        if lexeme_type == 'delimiter':
            self.tree += "\nParser Error: Expected delimeter '{}', got '{}' " \
                         "at line {}, column {}".format(expected, actual, line, column)
            return
        if lexeme_type == 'attribute':
            self.tree += "\nParser Error: Expected attribute like '{}', got '{}' " \
                         "at line {}, column {}".format(expected, actual, line, column)

    def print_tree(self):
        print(self.tree)

    def advance_lexeme(self):
        return self.lexemes.pop(0)

    def append_to_tree(self, node):
        self.tree += '.' * self.shift * 2 + node + '\n'

    @property
    def current_lexeme(self):
        return self.lexemes[0]
