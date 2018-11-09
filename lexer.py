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
        self.symbol_counter = 0
        self.column = 0
        self.line = 0

    def parse_string(self, string, callback=print):
        self.column = 1
        self.symbol_counter = 0
        self.line = 1
        self.text = string
        identifiers_code = 1001
        previous_lexeme = ''
        lexeme = ''
        begin_lexeme = 0
        while True:
            # READY STATE
            if self.current_state == READY_STATE:
                symbol = self.peek()
                if not symbol:
                    print("EOF")
                    break
                if symbol == '(':
                    self.current_state = BEGIN_COMMENT_STATE
                    begin_lexeme = self.column
                    symbol = self.pop()
                    lexeme += symbol
                    continue
                if symbol in delimiters.keys():
                    self.current_state = DELIMITER_STATE
                    begin_lexeme = self.column
                    symbol = self.pop()
                    lexeme += symbol
                    continue
                if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z':
                    self.current_state = IDENTIFIER_STATE
                    begin_lexeme = self.column
                    symbol = self.pop()
                    lexeme += symbol
                    continue
                if symbol in whitespaces:
                    if symbol == '\n':
                        self.line += 1
                        self.column = 1
                    symbol = self.pop()
                    continue
                self.current_state = ERROR_STATE
                begin_lexeme = self.column
                lexeme += symbol
                symbol = self.pop()
                continue

            # IDENTIFIER STATE
            if self.current_state == IDENTIFIER_STATE:
                symbol = self.peek()
                if not symbol:
                    if lexeme in keywords.keys():
                        callback("{0}\t{1}\t{2}\t{3}".format(
                            self.line, begin_lexeme, keywords[lexeme], lexeme
                        ))
                        # callback("KEYWORD: {0}\n line: {1}, column: {2}".format(
                        #     lexeme, str(self.line), str(begin_lexeme)))
                    else:
                        callback("{0}\t{1}\t{2}\t{3}".format(
                            self.line, begin_lexeme, identifiers_code, lexeme
                        ))
                        # callback("IDENTIFIER: {0}\n line: {1}, column: {2}".format(
                        #     lexeme, str(self.line), str(begin_lexeme)))
                        identifiers[lexeme] = identifiers_code
                        identifiers_code += 1

                    self.current_state = READY_STATE
                    lexeme = ''
                    continue

                if 'A' <= symbol <= 'Z' or 'a' <= symbol <= 'z' or '0' <= symbol <= '9':
                    symbol = self.pop()
                    lexeme += symbol
                    continue
                if lexeme in keywords.keys():
                    callback("{0}\t{1}\t{2}\t{3}".format(
                        self.line, begin_lexeme, keywords[lexeme], lexeme
                    ))
                    # callback("KEYWORD: {0}\n line: {1}, column: {2}".format(
                    #     lexeme, str(self.line), str(begin_lexeme)))
                else:
                    callback("{0}\t{1}\t{2}\t{3}".format(
                        self.line, begin_lexeme, identifiers_code, lexeme
                    ))
                    # callback("IDENTIFIER: {0}\n line: {1}, column: {2}".format(
                    #     lexeme, str(self.line), str(begin_lexeme)))
                    identifiers[lexeme] = identifiers_code
                    identifiers_code += 1

                self.current_state = READY_STATE
                lexeme = ''
                continue

            # DELIMITER STATE
            if self.current_state == DELIMITER_STATE:
                callback("{0}\t{1}\t{2}\t{3}".format(
                    self.line, begin_lexeme, delimiters[lexeme], lexeme
                ))
                # callback("DELIMITER: {0}\n line: {1}, column: {2}".format(
                #     lexeme, str(self.line), str(begin_lexeme)))
                self.current_state = READY_STATE
                lexeme = ''
                continue

            # SECOND DELIMITER STATE
            if self.current_state == SECOND_DELIMITER_STATE:
                callback("{0}\t{1}\t{2}\t{3}".format(
                    self.line, begin_lexeme, delimiters[lexeme], lexeme
                ))
                # callback("DELIMITER: {0}\n line: {1}, column: {2}".format(
                #     lexeme, str(self.line), str(begin_lexeme)))
                self.current_state = READY_STATE
                lexeme = ''
                continue

            # ERROR STATE
            if self.current_state == ERROR_STATE:
                self.current_state = READY_STATE
                if previous_lexeme == '*':
                    callback("Error: Unexpected EOF inside the comment, line : {0}, column: {1}".format(
                        self.line, begin_lexeme))
                    previous_lexeme = ''
                    continue
                callback("Error: Unmatched input ('{0}'), line: {1}, column: {2}".format(
                             lexeme, self.line, begin_lexeme))
                lexeme = ''
                continue

            # BEGIN COMMENT STATE
            if self.current_state == BEGIN_COMMENT_STATE:
                symbol = self.peek()
                if symbol != '*':
                    self.current_state = SECOND_DELIMITER_STATE
                    continue
                self.current_state = COMMENT_STATE
                symbol = self.pop()
                previous_lexeme += symbol
                lexeme = ''
                continue

            # COMMENT STATE
            if self.current_state == COMMENT_STATE:
                symbol = self.peek()
                if symbol == '*':
                    self.current_state = END_COMMENT_STATE
                    symbol = self.pop()
                    continue
                if not symbol:
                    self.current_state = ERROR_STATE
                    begin_lexeme = self.column
                    continue
                symbol = self.pop()
                continue

            # END COMMENT STATE
            if self.current_state == END_COMMENT_STATE:
                symbol = self.peek()
                if symbol == ')':
                    self.current_state = READY_STATE
                    symbol = self.pop()
                    continue
                if symbol != '*':
                    self.current_state = COMMENT_STATE
                    symbol = self.pop()
                    continue
                if not symbol:
                    self.current_state = ERROR_STATE
                    begin_lexeme = self.column
                    continue
                symbol = self.pop()
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
