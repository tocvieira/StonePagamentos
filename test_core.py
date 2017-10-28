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
        report = fromstring(get_stone_report("20171026"))
        self.assertEqual(get_gross_amount(report), 2501.0)

    def test_get_net_amount(self):
        report = fromstring(get_stone_report("20171026"))
        self.assertEqual(get_net_amount(report), 2426.3579999999997)

    def test_get_prevision(self):
        report = fromstring(get_stone_report("20171026"))
        prevision_date = len(builtins.dict(get_prevision(report)))
        self.assertEqual(prevision_date, 5)


if __name__ == '__main__':
    unittest.main()


