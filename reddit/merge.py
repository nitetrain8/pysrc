"""

Created by: Nathan Starkweather
Created on: 03/03/2014
Created in: PyCharm Community Edition


"""

def greater(a, b):
    if a > b:
        return a
    return b


def merge_sort(first, second):
    if not first:
        return second
    if not second:
        return first
    if first[0] > second[0]:
        result = second[0]
        return result + merge_sort(first, second[1:])
    else:
        result = first[0]
        return result + merge_sort(first[1:], second)


def do_merge(chars):
    lc = len(chars) // 2
    if not lc:
        return chars
    fh = chars[:lc]
    sh = chars[lc:]
    return merge_sort(do_merge(fh), do_merge(sh))



if __name__ == '__main__':

    import unittest

    class MergeTest(unittest.TestCase):

        def test_merge_sort_static(self):

            strs = (
                    ('ace', 'bst', 'abcest'),
                    ('uw', 'envz', 'enuvwz'),
                    ('', 'boe', 'boe'))

            for str1, str2, expected_result in strs:
                result = merge_sort(str1, str2)
                self.assertEqual(result, expected_result)
                self.assertEqual(do_merge(str1+str2), ''.join(sorted(str1+str2)))

        def test_merge_sort_random(self):
            import random

            alphabet = "abcdefghijklmnopqrstuvwxyz"

            for test in range(10000000):
                str1 = ''.join(alphabet[random.randint(i, 25)] for i in range(8))
                str2 = ''.join(alphabet[random.randint(i, 25)] for i in range(8))

                # my merge sort assumes both lists are already sorted, so we cheat
                len1 = len(str1)
                len2 = len(str2)
                str11 = ''.join(sorted(str1))
                str12 = ''.join(sorted(str2))
                result = merge_sort(str11, str12)
                expected_result = ''.join(sorted(str1 + str2))
                self.assertEqual(result, expected_result, str1 + str2)

                result2 = do_merge(str1+str2)
                self.assertEqual(result2, expected_result)
                if not test % 1000:
                    print(test)


    unittest.main()

