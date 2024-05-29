import unittest
from src.main import add


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 5), 8)
        self.assertEqual(add(-3, 2), -1)


if __name__ == '__main__':
    unittest.main()