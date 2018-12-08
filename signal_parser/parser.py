from tables import *


class Parser:
    def __init__(self, lexemes):
        self.i = 0
        self.shift = 0
        self.lexemes = lexemes
        self.tree = ''

    def signal_program(self):
        self.tree += '<signal-program>\n'
        self.shift += 2
        self.program()
        self.shift -= 2

    def program(self):
        lexeme = self.lexemes.pop(self.i)
        if lexeme.code != keywords["PROGRAM"]:
            print("Parser Error: Keyword 'PROGRAM' "
                  "expected at line {0}, column {1}".format(lexeme.line, lexeme.column))
            return
        else:
            self.add_spaces(self.shift)
            self.tree += '<program>\n'
            self.shift += 2
            self.add_spaces(self.shift)
            self.tree += '{0} {1}'.format(lexeme.code, lexeme.value)

        #     self.procedure_identifier()
        # if lexeme.code != constants[";"]:
        #     return "Parser Error: Delimiter ';' expected " \
        #            "at line {0}, column {1}".format(lexeme.line, lexeme.column)

    def procedure_identifier(self):
        pass

    def block(self):
        pass

    def declarations(self):
        pass

    def statements_list(self):
        pass

    def procedure_declarations(self):
        pass

    def procedure(self):
        pass

    def parameters_list(self):
        pass

    def declarations_list(self):
        pass

    def declaration(self):
        pass

    def variable_identifier(self):
        pass

    def add_spaces(self, spaces):
        for i in range(spaces):
            self.tree += '.'

    def print_tree(self):
        print(self.tree)
