import unittest
from tables import identifiers
from lexer import Lexer


class TestParse(unittest.TestCase):
    def test_identifiers(self):
        strings = ['Hello Worlds', 'HelloWorlds', 'F0gtefes', 'Addd ddfg bbbn']
        valid_identifiers = [
            {'Hello', 'Worlds'},
            {'HelloWorlds'},
            {'F0gtefes'},
            {'Addd', 'ddfg', 'bbbn'}
        ]
        lexer = Lexer()
        for string, valid_idns in zip(strings, valid_identifiers):
            lexer.parse_string(string)
            self.assertEqual(identifiers, valid_idns)
            identifiers.clear()

    # def test_delimiters(self):
    #     self.assertEqual(True, False)
    #
    # def test_comments(self):
    #     self.assertEqual(True, False)
    #
    def test_phrases(self):
        strings = ['PROGRAM Hello;', 'BEGIN PROCEDURE this bla; bla; bla; END;']
        self.assertEqual(True, False)

    # def test_failures(self):
    #     self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
