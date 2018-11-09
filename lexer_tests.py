import unittest
from tables import identifiers
from lexer import Lexer


class TestParse(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestParse, self).__init__(*args, **kwargs)
        self.tokens = []

    def lexer_callback(self, token):
        self.tokens.append(token)

    def test_identifiers(self):
        strings = [
            'Hello Worlds',
            'HelloWorlds',
            'aabbb00 dd123db sssd',
            'Some test\nanother'
        ]
        valid_identifiers = [
            {'Hello', 'Worlds'},
            {'HelloWorlds'},
            {'aabbb00', 'dd123db', 'sssd'},
            {'Some', 'test', 'another'}
        ]
        valid_tokens = [
            ['IDENTIFIER: Hello\n line: 1, column: 1',
             'IDENTIFIER: Worlds\n line: 1, column: 7'],
            ['IDENTIFIER: HelloWorlds\n line: 1, column: 1'],
            ['IDENTIFIER: aabbb00\n line: 1, column: 1',
             'IDENTIFIER: dd123db\n line: 1, column: 9',
             'IDENTIFIER: sssd\n line: 1, column: 17'],
            ['IDENTIFIER: Some\n line: 1, column: 1',
             'IDENTIFIER: test\n line: 1, column: 6',
             'IDENTIFIER: another\n line: 2, column: 1']
        ]
        lexer = Lexer()
        for string, valid_idns, valid_token in zip(strings, valid_identifiers, valid_tokens):
            lexer.parse_string(string, self.lexer_callback)
            self.assertEqual(identifiers, valid_idns)
            self.assertEqual(
                self.tokens,
                valid_token)
            identifiers.clear()
            self.tokens.clear()

    def test_keywords(self):
        strings = [
            'PROGRAM hello',
            'program Hello',
            'SIGNAL sig',
            'LINK nolink'
        ]
        valid_identifiers = [
            {'hello'},
            {'program', 'Hello'},
            {'sig'},
            {'LINK', 'nolink'}
        ]
        valid_tokens = [
            ['KEYWORD: PROGRAM\n line: 1, column: 1',
             'IDENTIFIER: hello\n line: 1, column: 9'],
            ['IDENTIFIER: program\n line: 1, column: 1',
             'IDENTIFIER: Hello\n line: 1, column: 9'],
            ['KEYWORD: SIGNAL\n line: 1, column: 1',
             'IDENTIFIER: sig\n line: 1, column: 8'],
            ['IDENTIFIER: LINK\n line: 1, column: 1',
             'IDENTIFIER: nolink\n line: 1, column: 6']
        ]
        lexer = Lexer()
        for string, valid_idns, valid_token in zip(strings, valid_identifiers, valid_tokens):
            lexer.parse_string(string, self.lexer_callback)
            self.assertEqual(identifiers, valid_idns)
            self.assertEqual(
                self.tokens,
                valid_token)
            identifiers.clear()
            self.tokens.clear()

    def test_delimiters(self):
        strings = [
            ';;;; ,,, :: ()'
        ]
        valid_identifiers = [
            set()
        ]
        valid_tokens = [
            ['DELIMITER: ;\n line: 1, column: 1',
             'DELIMITER: ;\n line: 1, column: 2',
             'DELIMITER: ;\n line: 1, column: 3',
             'DELIMITER: ;\n line: 1, column: 4',
             'DELIMITER: ,\n line: 1, column: 6',
             'DELIMITER: ,\n line: 1, column: 7',
             'DELIMITER: ,\n line: 1, column: 8',
             'DELIMITER: :\n line: 1, column: 10',
             'DELIMITER: :\n line: 1, column: 11',
             'DELIMITER: (\n line: 1, column: 13',
             'DELIMITER: )\n line: 1, column: 14']
        ]
        lexer = Lexer()
        for string, valid_idns, valid_token in zip(strings, valid_identifiers, valid_tokens):
            lexer.parse_string(string, self.lexer_callback)
            self.assertEqual(identifiers, valid_idns)
            self.assertEqual(
                self.tokens,
                valid_token)
            identifiers.clear()
            self.tokens.clear()

    def test_comments(self):
        strings = [
            '(* Let it be comment *)',
            '(**** Get * some * stars!!! ****)',
            '(****///\\\***)',
        ]
        valid_identifiers = [
            set()
        ]
        valid_tokens = [
            []
        ]
        lexer = Lexer()
        for string, valid_idns, valid_token in zip(strings, valid_identifiers, valid_tokens):
            lexer.parse_string(string, self.lexer_callback)
            self.assertEqual(identifiers, valid_idns)
            self.assertEqual(
                self.tokens,
                valid_token)
            identifiers.clear()
            self.tokens.clear()

    def test_phrases(self):
        strings = [
            'PROGRAM Hello;',
            'BEGIN\n'
            'PROCEDURE this\n'
            'bla;\n'
            'bla;\n'
            'bla;\n'
            'END',
            '(* This is first program *)\n'
            'PROGRAM HelloWorld1;\n'
            'BEGIN\n'
            'PROCEDURE proc:(tell, well, sell);\n'
            'INTEGER terra:tell;\n'
            'BLOCKFLOAT rec0rd1:well;\n'
            'SIGNAL sig:sell;\n'
            'END\n'
            'EXT'
        ]
        valid_identifiers = [
            {'Hello'},
            {'this', 'bla', 'bla', 'bla'},
            {'HelloWorld1', 'proc', 'tell', 'well', 'sell',
             'terra', 'tell', 'rec0rd1', 'well', 'sig', 'sell'}
        ]
        valid_tokens = [
            ['KEYWORD: PROGRAM\n line: 1, column: 1',
             'IDENTIFIER: Hello\n line: 1, column: 9',
             'DELIMITER: ;\n line: 1, column: 14'],

            ['KEYWORD: BEGIN\n line: 1, column: 1',

             'KEYWORD: PROCEDURE\n line: 2, column: 1',
             'IDENTIFIER: this\n line: 2, column: 11',

             'IDENTIFIER: bla\n line: 3, column: 1',
             'DELIMITER: ;\n line: 3, column: 4',

             'IDENTIFIER: bla\n line: 4, column: 1',
             'DELIMITER: ;\n line: 4, column: 4',

             'IDENTIFIER: bla\n line: 5, column: 1',
             'DELIMITER: ;\n line: 5, column: 4',

             'KEYWORD: END\n line: 6, column: 1'
             ],
            ['KEYWORD: PROGRAM\n line: 2, column: 1',
             'IDENTIFIER: HelloWorld1\n line: 2, column: 9',
             'DELIMITER: ;\n line: 2, column: 20',

             'KEYWORD: BEGIN\n line: 3, column: 1',

             'KEYWORD: PROCEDURE\n line: 4, column: 1',
             'IDENTIFIER: proc\n line: 4, column: 11',
             'DELIMITER: :\n line: 4, column: 15',
             'DELIMITER: (\n line: 4, column: 16',
             'IDENTIFIER: tell\n line: 4, column: 17',
             'DELIMITER: ,\n line: 4, column: 21',
             'IDENTIFIER: well\n line: 4, column: 23',
             'DELIMITER: ,\n line: 4, column: 27',
             'IDENTIFIER: sell\n line: 4, column: 29',
             'DELIMITER: )\n line: 4, column: 33',
             'DELIMITER: ;\n line: 4, column: 34',

             'KEYWORD: INTEGER\n line: 5, column: 1',
             'IDENTIFIER: terra\n line: 5, column: 9',
             'DELIMITER: :\n line: 5, column: 14',
             'IDENTIFIER: tell\n line: 5, column: 15',
             'DELIMITER: ;\n line: 5, column: 19',

             'KEYWORD: BLOCKFLOAT\n line: 6, column: 1',
             'IDENTIFIER: rec0rd1\n line: 6, column: 12',
             'DELIMITER: :\n line: 6, column: 19',
             'IDENTIFIER: well\n line: 6, column: 20',
             'DELIMITER: ;\n line: 6, column: 24',

             'KEYWORD: SIGNAL\n line: 7, column: 1',
             'IDENTIFIER: sig\n line: 7, column: 8',
             'DELIMITER: :\n line: 7, column: 11',
             'IDENTIFIER: sell\n line: 7, column: 12',
             'DELIMITER: ;\n line: 7, column: 16',

             'KEYWORD: END\n line: 8, column: 1',

             'KEYWORD: EXT\n line: 9, column: 1',
             ]
        ]
        lexer = Lexer()
        for string, valid_idns, valid_token in zip(strings, valid_identifiers, valid_tokens):
            lexer.parse_string(string, self.lexer_callback)
            self.assertEqual(identifiers, valid_idns)
            self.assertEqual(
                self.tokens,
                valid_token)
            identifiers.clear()
            self.tokens.clear()

    def test_failures(self):
        strings = [
            '(* Let it be....',
            '(****',
            '4abbc',
            '23657',
            '***)',
            'abbb//cd',
            '\\ // . `?',
            'program notkeyword',

        ]
        valid_identifiers = [
            set(),
            set(),
            {'abbc'},
            set(),
            set(),
            {'abbb', 'cd'},
            set(),
            {'program', 'notkeyword'}
        ]
        valid_tokens = [
            ['Error: Unexpected EOF inside the comment, line : 1, column: 17'],
            ['Error: Unexpected EOF inside the comment, line : 1, column: 6'],
            [
                'Error: Unmatched input (\'4\'), line: 1, column: 1',
                'IDENTIFIER: abbc\n line: 1, column: 2'
            ],
            [
                'Error: Unmatched input (\'2\'), line: 1, column: 1',
                'Error: Unmatched input (\'3\'), line: 1, column: 2',
                'Error: Unmatched input (\'6\'), line: 1, column: 3',
                'Error: Unmatched input (\'5\'), line: 1, column: 4',
                'Error: Unmatched input (\'7\'), line: 1, column: 5',
            ],
            [
                'Error: Unmatched input (\'*\'), line: 1, column: 1',
                'Error: Unmatched input (\'*\'), line: 1, column: 2',
                'Error: Unmatched input (\'*\'), line: 1, column: 3',
                'DELIMITER: )\n line: 1, column: 4',
            ],
            [
                'IDENTIFIER: abbb\n line: 1, column: 1',
                'Error: Unmatched input (\'/\'), line: 1, column: 5',
                'Error: Unmatched input (\'/\'), line: 1, column: 6',
                'IDENTIFIER: cd\n line: 1, column: 7'
            ],
            [
                'Error: Unmatched input (\'\\\'), line: 1, column: 1',
                'Error: Unmatched input (\'/\'), line: 1, column: 3',
                'Error: Unmatched input (\'/\'), line: 1, column: 4',
                'Error: Unmatched input (\'.\'), line: 1, column: 6',
                'Error: Unmatched input (\'`\'), line: 1, column: 8',
                'Error: Unmatched input (\'?\'), line: 1, column: 9',
            ],
            [
                'IDENTIFIER: program\n line: 1, column: 1',
                'IDENTIFIER: notkeyword\n line: 1, column: 9'
            ]
        ]
        lexer = Lexer()
        for string, valid_idns, valid_token in zip(strings, valid_identifiers, valid_tokens):
            lexer.parse_string(string, self.lexer_callback)
            self.assertEqual(identifiers, valid_idns)
            self.assertEqual(
                self.tokens,
                valid_token)
            identifiers.clear()
            self.tokens.clear()


if __name__ == '__main__':
    unittest.main()
