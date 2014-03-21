__author__ = 'Administrator'

import unittest
from os.path import join, dirname, split, splitext
from os import makedirs as mkdirs
from shutil import rmtree

from pysrc.mycompiler.parser.preprocess import parse_line, parse_stream, Directive, \
    FlowCtrl, Include, filter_directives

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

        pre_pends = "#", " #", "# ", "   #   "
        post_pends = "\n", " \n", " foo\n", "(bar)\n", "\n", " f\n", """ do { \\
        foo.bar = baz; \\
        } while(0);
        """
        base_kw = ("include", "if", "define", "endif", "undef")

        # Generate test lines
        test_lines = []
        for kw in base_kw:
            for pre in pre_pends:
                for post in post_pends:
                    line = (''.join((pre, kw, post)), kw, post)
                    test_lines.append(line)

        self.test_lines = test_lines
        self.pre_pends = pre_pends
        self.post_pends = post_pends
        self.base_kw = base_kw

    def test_parse_line_match(self):
        """
        @return:
        @rtype:
        """

        parse = parse_line

        for raw, kw, post in self.test_lines:
            result = parse(raw)
            self.assertIsNot(result, None, raw)
            name, args, value, multiline = result
            self.assertEqual(name, kw, "Name Mismatch")

    def test_parse_line_match_defined(self):
        """
        @return:
        @rtype:
        """
        test_str = "#if defined (__vax__) || defined (__ns16000__)"

        from re import compile as re_compile, DOTALL

        valid_dir = '(%s)' % '|'.join(Directive.VALID)

        id_or_arg = r"(\((.+)\)|(\|\||&&)|[a-zA-Z][a-zA-Z0-0_]*)"

        arg = "defined (__vax__) || defined (__ns16000__)"
        arg2 = "(__vax__) || defined (__ns16000__)"
        arg3 = "defined || bar (__foobaz__)"
        myre = r'\s*'.join(('', '#', valid_dir, id_or_arg))


        result = parse_line(test_str)



    def test_iterlines(self):
        """
        @return:
        @rtype:
        """

        # filter_directives requires a file object, so write test code to
        # StringIO() for testing

        def rewind(fobj):
            """
            @type fobj: typehint.FileObject
            """
            fobj.seek(0, 0)  # SEEK_SET

        from io import StringIO
        fbuf = StringIO()

        multi_test = ("#define herpadperp do { \\", "\t\t\t foo.bar = baz; \\", "\t\t\t} while(0);")

        tests = (
            ("#include <stdio.h>", ("include", " <stdio.h>")),
            ("#if defined (__vax__) \\\n|| defined (__ns16000__)", ("if", "defined (__vax__) || defined (__ns16000__)")),
            ('\n'.join(multi_test), ("herpaderp", ""))
        )

        for line, result in tests:
            fbuf = StringIO(line)
            rewind(fbuf)

            gen = filter_directives(fbuf)
            for r in gen:
                print(repr(r))


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
