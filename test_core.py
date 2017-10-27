import unittest
import hashlib
from core import *

class StoneTest(unittest.TestCase):

    def test_get_stone_report(self):
        r = get_stone_report("20171026")
        h = hashlib.sha1(r.encode('utf-8'))
        hexrhash = h.hexdigest()
        defaulth = "1d6ad2ea634514c7ef6225fd15c332cb52ed45fd"
        self.assertEqual(hexrhash,defaulth)

    def test_get_gross_amount(self):
        pass

if __name__ == '__main__':
    unittest.main()

