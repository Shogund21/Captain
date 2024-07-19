import unittest
from src.chroma import setup_chroma

class TestChroma(unittest.TestCase):
    def test_setup_chroma(self):
        collection = setup_chroma()
        self.assertIsNotNone(collection)

if __name__ == '__main__':
    unittest.main()
