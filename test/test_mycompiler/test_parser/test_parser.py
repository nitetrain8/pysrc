__author__ = 'Administrator'

import unittest
from os.path import join, dirname, split, splitext
from os import makedirs as mkdirs
from shutil import rmtree

from pysrc.mycompiler.parser.preprocess import parse_line, parse_stream

curdir, module = split(__file__)
module, _ = splitext(module)
input_dir = join(curdir, 'files')
test_dir = dirname(dirname(curdir))
temp_dir = join(test_dir, 'temp', 'test_parser')


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """
        @return: None
        @rtype: None
        """
        try:
            mkdirs(temp_dir)
        except FileExistsError:
            pass

    def test_parse_line_match(self):
        """
        @return:
        @rtype:
        """

        parse = parse_line

        pre_pends = "#", " #", "# ", "   #   "
        post_pends = "\n", " \n", " foo\n", "(bar)\n", "\n", " f\n", """ do { \\
foo.bar = baz; \\
} while(0);
"""
        base_kw = ("include", "if", "define", "endif", "undef")

        test_lines = []
        for kw in base_kw:
            for pre in pre_pends:
                for post in post_pends:
                    line = (''.join((pre, kw, post)), kw, post)
                    test_lines.append(line)

        #for raw, result in test_lines[7::7]:
        for raw, kw, post in test_lines:
            result = parse(raw)
            self.assertIsNot(result, None, raw)
            name, args, value, multiline = result
            self.assertEqual(name, kw, "Name Mismatch")
            print(result)




    def tearDown(self):
        """
        @return: None
        @rtype: None
        """
        try:
            rmtree(temp_dir)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()
