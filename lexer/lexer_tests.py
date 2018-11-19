import unittest
from tables import identifiers, constants
from lexer import Lexer


class TestParse(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestParse, self).__init__(*args, **kwargs)
        self.tokens = []

    def lexer_callback(self, token):
        self.tokens.append(token)

    def test_identifiers(self):
        identifier_file = open("identifiers.txt", "r")
        identifiers_samples = identifier_file.read()
        valid_identifiers = {'Hello': 1001, 'Worlds': 1002, 'HelloWorlds': 1003, 'aabbb00': 1004,
                             'dd123db': 1005, 'sssd': 1006, 'Some': 1007, 'test': 1008, 'another': 1009}
        valid_constants = dict()
        valid_tokens = [
            '1\t1\t1001\tHello',
            '1\t7\t1002\tWorlds',
            '2\t1\t1003\tHelloWorlds',
            '3\t1\t1004\taabbb00',
            '3\t9\t1005\tdd123db',
            '3\t17\t1006\tsssd',
            '4\t1\t1007\tSome',
            '4\t6\t1008\ttest',
            '5\t1\t1009\tanother'
        ]
        lexer = Lexer()
        lexer.parse_string(identifiers_samples, self.lexer_callback)
        self.assertEqual(identifiers, valid_identifiers)
        self.assertEqual(constants, valid_constants)
        self.assertEqual(self.tokens, valid_tokens)
        identifiers.clear()
        constants.clear()
        identifier_file.close()

    def test_keywords(self):
        keyword_file = open("keywords.txt", "r")
        keywords_samples = keyword_file.read()
        valid_identifiers = {'hello': 1001, 'program': 1002, 'Hello': 1003, 'sig': 1004,
                             'LINK': 1005, 'nolink': 1006}
        valid_constants = dict()
        valid_tokens = [
            '1\t1\t401\tPROGRAM',
            '1\t9\t1001\thello',
            '2\t1\t1002\tprogram',
            '2\t9\t1003\tHello',
            '3\t1\t405\tSIGNAL',
            '3\t8\t1004\tsig',
            '4\t1\t1005\tLINK',
            '4\t6\t1006\tnolink'
        ]
        lexer = Lexer()
        lexer.parse_string(keywords_samples, self.lexer_callback)
        self.assertEqual(identifiers, valid_identifiers)
        self.assertEqual(constants, valid_constants)
        self.assertEqual(self.tokens, valid_tokens)
        identifiers.clear()
        constants.clear()
        keyword_file.close()

    def test_delimiters(self):
        delimiter_file = open("delimiters.txt", "r")
        delimiters_samples = delimiter_file.read()
        valid_identifiers = dict()
        valid_constants = dict()
        valid_tokens = [
            '1\t1\t59\t;',
            '1\t2\t59\t;',
            '1\t3\t59\t;',
            '1\t4\t59\t;',
            '1\t5\t59\t;',
            '2\t1\t44\t,',
            '2\t2\t44\t,',
            '2\t3\t44\t,',
            '2\t4\t44\t,',
            '3\t1\t58\t:',
            '3\t2\t58\t:',
            '4\t1\t40\t(',
            '4\t2\t41\t)',
            'Error: Unmatched input (\'.\'), line: 5, column: 1',
            'Error: Unmatched input (\'.\'), line: 5, column: 2',
            'Error: Unmatched input (\'.\'), line: 5, column: 3'
        ]
        lexer = Lexer()
        lexer.parse_string(delimiters_samples, self.lexer_callback)
        self.assertEqual(identifiers, valid_identifiers)
        self.assertEqual(constants, valid_constants)
        self.assertEqual(self.tokens, valid_tokens)
        identifiers.clear()
        constants.clear()
        delimiter_file.close()

    def test_comments(self):
        comment_file = open("comments.txt", "r")
        comments_samples = comment_file.read()
        valid_identifiers = dict()
        valid_constants = dict()
        valid_tokens = []
        lexer = Lexer()
        lexer.parse_string(comments_samples, self.lexer_callback)
        self.assertEqual(identifiers, valid_identifiers)
        self.assertEqual(constants, valid_constants)
        self.assertEqual(self.tokens, valid_tokens)
        identifiers.clear()
        constants.clear()
        comment_file.close()

    def test_phrases(self):
        phrases_file = open("phrases.txt", "r")
        phrases_samples = phrases_file.read()
        valid_identifiers = {'Hello': 1001, 'this': 1002, 'bla': 1003}
        valid_constants = {'123': 501, '44': 502}
        valid_tokens = [
            '1\t1\t401\tPROGRAM',
            '1\t9\t1001\tHello',
            '1\t14\t59\t;',
            '2\t5\t402\tBEGIN',
            '3\t5\t403\tPROCEDURE',
            '3\t15\t1002\tthis',
            '4\t9\t1003\tbla',
            '4\t13\t501\t123',
            '4\t16\t59\t;',
            '5\t9\t1003\tbla',
            '5\t12\t59\t;',
            '6\t9\t1003\tbla',
            '6\t13\t502\t44',
            '6\t15\t59\t;',
            '7\t5\t404\tEND'
        ]
        lexer = Lexer()
        lexer.parse_string(phrases_samples, self.lexer_callback)
        self.assertEqual(identifiers, valid_identifiers)
        self.assertEqual(constants, valid_constants)
        self.assertEqual(self.tokens, valid_tokens)
        identifiers.clear()
        constants.clear()
        phrases_file.close()

    def test_failures(self):
        failure_file = open("failures.txt", "r")
        failures_samples = failure_file.read()
        valid_identifiers = {'abbb': 1001, 'cd': 1002, 'program': 1003, 'notkeyword': 1004}
        valid_constants = dict()
        valid_tokens = [
            'Error: Unmatched input (\'4abbc\'), line: 1, column: 1',
            'Error: Unmatched input (\'12bbb555\'), line: 2, column: 1',
            'Error: Unmatched input (\'*\'), line: 3, column: 1',
            'Error: Unmatched input (\'*\'), line: 3, column: 2',
            'Error: Unmatched input (\'*\'), line: 3, column: 3',
            '3\t4\t41\t)',
            '4\t1\t1001\tabbb',
            'Error: Unmatched input (\'/\'), line: 4, column: 5',
            'Error: Unmatched input (\'/\'), line: 4, column: 6',
            '4\t7\t1002\tcd',
            'Error: Unmatched input (\'\\\'), line: 5, column: 1',
            'Error: Unmatched input (\'\\\'), line: 5, column: 2',
            'Error: Unmatched input (\'/\'), line: 5, column: 4',
            'Error: Unmatched input (\'/\'), line: 5, column: 5',
            'Error: Unmatched input (\'.\'), line: 5, column: 7',
            'Error: Unmatched input (\'`\'), line: 5, column: 9',
            'Error: Unmatched input (\'?\'), line: 5, column: 10',
            '6\t1\t1003\tprogram',
            '6\t9\t1004\tnotkeyword',
            'Error: Unexpected EOF inside the comment, line : 7, column: 17'
        ]
        lexer = Lexer()
        lexer.parse_string(failures_samples, self.lexer_callback)
        self.assertEqual(identifiers, valid_identifiers)
        self.assertEqual(constants, valid_constants)
        self.assertEqual(self.tokens, valid_tokens)
        identifiers.clear()
        constants.clear()
        failure_file.close()


if __name__ == '__main__':
    unittest.main()
