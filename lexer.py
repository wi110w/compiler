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
        self.i = 0

    def parse_string(self, string):
        self.i = 0
        self.text = string
        lexeme = ''
        while True:
            if self.current_state == READY_STATE:
                symbol = self.peek()
                if not symbol:
                    break
                if symbol in delimiters:
                    self.current_state = DELIMITER_STATE
                    symbol = self.pop()
                    lexeme += symbol
                elif 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
                    self.current_state = IDENTIFIER_STATE
                    symbol = self.pop()
                    lexeme += symbol
                elif symbol in whitespaces:
                    symbol = self.pop()
                continue
            if self.current_state == IDENTIFIER_STATE:
                symbol = self.peek()
                if not symbol:
                    if lexeme in keywords:
                        print("KEYWORD: " + lexeme)
                    else:
                        print("IDENTIFIER: " + lexeme)
                        identifiers.add(lexeme)

                    self.current_state = READY_STATE
                    lexeme = ''

                elif 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
                    symbol = self.pop()
                    lexeme += symbol
                else:
                    if lexeme in keywords:
                        print("KEYWORD: " + lexeme)
                    else:
                        print("IDENTIFIER: " + lexeme)
                        identifiers.add(lexeme)

                    self.current_state = READY_STATE
                    lexeme = ''
                continue
            if self.current_state == DELIMITER_STATE:
                print("DELIMITER: " + lexeme)
                self.current_state = READY_STATE
                lexeme = ''
                continue

    def peek(self):
        if self.i >= len(self.text):
            return None
        return self.text[self.i]

    def pop(self):
        if self.i >= len(self.text):
            return None
        symbol = self.text[self.i]
        self.i += 1
        return symbol
