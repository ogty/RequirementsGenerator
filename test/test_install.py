import unittest

from main import is_install


class TestInstall(unittest.TestCase):
    
    def test_install_ok(self):
        self.assertTrue(is_install("python-dotenv"))

    def test_install_no(self):
        self.assertFalse(is_install("dotenv"))

if __name__ == "__main__":
    unittest.main()
