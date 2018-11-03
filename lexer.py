from states import *
from tables import *

'''
* Peek and Pop
* For identifier state:
* In ready state we peek current symbol, so we don't get it, just look at it.
* If it's an alphabet symbol, from ready state to identifier state
* In identifier we pop that symbol and peek another symbol
* If it fits, we stay in those state, poping symbol
* If next symbol is other than need, in identifier state we start analyze identifier and print it
* Then go to ready state for next symbol
'''


class Lexer:
    def __init__(self):
        self.current_state = READY_STATE
        self.identifier = ''
        self.text = ''
        self.column = 0
        self.line = 0

    def parse_string(self, string):
        self.column = 0
        self.line = 0
        self.text = string
        lexeme = ''
        begin_lexeme = 0
        while True:
            if self.current_state == READY_STATE:
                symbol = self.peek()
                if not symbol:
                    print("EOF")
                    break
                if symbol in delimiters:
                    self.current_state = DELIMITER_STATE
                    begin_lexeme = self.column
                    symbol = self.pop()
                    lexeme += symbol
                elif 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
                    self.current_state = IDENTIFIER_STATE
                    begin_lexeme = self.column
                    symbol = self.pop()
                    lexeme += symbol
                elif symbol in whitespaces:
                    symbol = self.pop()
                else:
                    self.current_state = ERROR_STATE
                    begin_lexeme = self.column
                    lexeme += symbol
                    symbol = self.pop()
                continue
            if self.current_state == IDENTIFIER_STATE:
                symbol = self.peek()
                if not symbol:
                    if lexeme in keywords:
                        print("KEYWORD: " + lexeme + "\n Line: "
                              + str(self.line) + ', column: ' + str(begin_lexeme))
                    else:
                        print("IDENTIFIER: " + lexeme + "\n Line: "
                              + str(self.line) + ', column: ' + str(begin_lexeme))
                        identifiers.add(lexeme)

                    self.current_state = READY_STATE
                    lexeme = ''

                elif 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z' or '0' <= symbol <= '9':
                    symbol = self.pop()
                    lexeme += symbol
                else:
                    if lexeme in keywords:
                        print("KEYWORD: " + lexeme + "\n Line: "
                              + str(self.line) + ', column: ' + str(begin_lexeme))
                    else:
                        print("IDENTIFIER: " + lexeme + "\n Line: "
                              + str(self.line) + ', column: ' + str(begin_lexeme))
                        identifiers.add(lexeme)

                    self.current_state = READY_STATE
                    lexeme = ''
                continue
            if self.current_state == DELIMITER_STATE:
                print("DELIMITER: " + lexeme + "\n Line: "
                      + str(self.line) + ', column: ' + str(begin_lexeme))
                self.current_state = READY_STATE
                lexeme = ''
                continue
            if self.current_state == ERROR_STATE:
                self.current_state = READY_STATE
                print("Error: Unmatched input ('{0}'), line: {1}, column: {2}".format(
                             lexeme, self.line, begin_lexeme))
                lexeme = ''
                continue

    def peek(self):
        if self.column >= len(self.text):
            return None
        return self.text[self.column]

    def pop(self):
        if self.column >= len(self.text):
            return None
        symbol = self.text[self.column]
        self.column += 1
        return symbol
