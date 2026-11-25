import subprocess
import sys
import unittest


def cli(*args):
    return subprocess.run([sys.executable, "contrast_desk.py", *args], text=True, capture_output=True)


class ContrastDeskTests(unittest.TestCase):
    def test_black_and_white_pass_every_threshold(self):
        result = cli("#fff", "#000", "--require", "aaa")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("21.00:1", result.stdout)
        self.assertIn("Higher-contrast text: #FFFFFF", result.stdout)

    def test_identical_colors_fail_requested_threshold(self):
        result = cli("777", "777777", "--require", "aa")
        self.assertEqual(result.returncode, 1)
        self.assertIn("1.00:1", result.stdout)

    def test_alpha_color_is_rejected(self):
        result = cli("11223344", "fff")
        self.assertEqual(result.returncode, 2)
        self.assertIn("three- or six-digit hex color", result.stderr)
