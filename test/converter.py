import unittest

class Converter:
    @staticmethod
    def do(x: float) -> int:
        if x >= 100.7:
            return 1000
        elif x > 0.0:
            return int(x)
        elif x == 0.0:
            raise ValueError("x не может быть 0.0")
        elif x >= -30.4:
            return int(x) - 5
        else:
            return -2000



class TestConverter(unittest.TestCase):

    def test_positive_1(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_positive_2(self):
        self.assertEqual(Converter.do(100.6), 100)

    def test_0(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_negative_1(self):
        self.assertEqual(Converter.do(-30.4), -35)

    def test_negative_2(self):
        self.assertEqual(Converter.do(-30.5), -2000)



if __name__ == '__main__':
    unittest.main()