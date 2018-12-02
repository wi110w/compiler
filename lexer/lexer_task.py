from states import *
from tables import *
from lexeme import Lexeme


class LexerTask:
    def __init__(self):
        self.current_state = READY_STATE
        self.identifier = ''
        self.text = ''
        self.symbol_counter = 0
        self.column = 0
        self.line = 0

    def parse_string(self, string, callback=print):
        lexemes = []
        self.column = 1
        self.symbol_counter = 0
        self.line = 1
        self.text = string
        identifiers_code = 1001
        previous_lexeme = ''
        lexeme = ''
        begin_lexeme = 0
        alpha_lexeme = False
        while True:
            # READY STATE
            if self.current_state == READY_STATE:
                symbol = self.peek()
                if not symbol:
                    print("EOF")
                    lexemes.append(Lexeme(self.line, self.column, "EOF", 0))
                    break
                if symbol == 'X' or symbol == 'V':
                    self.current_state = BEGIN_IDENTIFIER_STATE
                    begin_lexeme = self.column
                    symbol = self.pop()
                    lexeme += symbol
                    continue
                if symbol in whitespaces:
                    if symbol == '\n':
                        self.line += 1
                        self.column = 1
                    if symbol == '\t':
                        self.column += 3
                    symbol = self.pop()
                    continue
                self.current_state = ERROR_STATE
                begin_lexeme = self.column
                lexeme += symbol
                symbol = self.pop()
                continue

            # BEGIN IDENTIFIER STATE
            if self.current_state == BEGIN_IDENTIFIER_STATE:
                symbol = self.peek()
                if not symbol or symbol in whitespaces:
                    self.current_state = ERROR_STATE
                    continue
                if symbol == '[':
                    self.current_state = IDENTIFIER_STATE
                    symbol = self.pop()
                    previous_lexeme = symbol
                    lexeme += symbol
                    continue

            # IDENTIFIER STATE
            if self.current_state == IDENTIFIER_STATE:
                symbol = self.peek()
                if not symbol or symbol in whitespaces:
                    self.current_state = ERROR_STATE
                    begin_lexeme = self.column
                    continue

                if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
                    lexeme += symbol
                    alpha_lexeme = True
                    symbol = self.pop()
                    continue

                if '0' <= symbol <= '9':
                    symbol = self.pop()
                    lexeme += symbol
                    continue

                if symbol == ']':
                    symbol = self.pop()
                    lexeme += symbol
                    if alpha_lexeme:
                        self.current_state = ERROR_STATE
                        previous_lexeme = ''
                        continue
                    self.current_state = READY_STATE
                    if lexeme in identifiers.keys():
                        callback("{0}\t{1}\t{2}\t{3}".format(
                            self.line, begin_lexeme, identifiers[lexeme], lexeme
                        ))
                    else:
                        callback("{0}\t{1}\t{2}\t{3}".format(
                            self.line, begin_lexeme, identifiers_code, lexeme
                        ))
                        lexemes.append(Lexeme(self.line, begin_lexeme, lexeme, identifiers_code))

                        identifiers[lexeme] = identifiers_code
                        identifiers_code += 1

                    lexeme = ''
                    continue

            # ERROR STATE
            if self.current_state == ERROR_STATE:
                self.current_state = READY_STATE
                if previous_lexeme == '[':
                    callback("Lexer Error: Unexpected EOF inside the comment, line : {0}, column: {1}".format(
                        self.line, begin_lexeme))
                    previous_lexeme = ''
                    lexeme = ''
                    continue
                callback("Lexer Error: Unmatched input ('{0}'), line: {1}, column: {2}".format(
                             lexeme, self.line, begin_lexeme))
                lexeme = ''
                continue

    def peek(self):
        if self.symbol_counter >= len(self.text):
            return None
        return self.text[self.symbol_counter]

    def pop(self):
        if self.symbol_counter >= len(self.text):
            return None
        symbol = self.text[self.symbol_counter]
        self.symbol_counter += 1
        if symbol != '\n':
            self.column += 1
        return symbol