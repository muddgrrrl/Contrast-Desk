#!/usr/bin/env python3
"""Check text contrast for two hexadecimal sRGB colors."""
import argparse
import re


def rgb(value):
    digits = value.removeprefix("#")
    if len(digits) not in (3, 6) or not re.fullmatch(r"[0-9a-fA-F]+", digits):
        raise argparse.ArgumentTypeError("enter a three- or six-digit hex color")
    if len(digits) == 3:
        digits = "".join(channel * 2 for channel in digits)
    return tuple(int(digits[i:i + 2], 16) for i in range(0, 6, 2))


def luminance(color):
    def linear(value):
        x = value / 255
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return sum(weight * linear(value) for weight, value in zip((0.2126, 0.7152, 0.0722), color))


def contrast(first, second):
    dark, bright = sorted((luminance(first), luminance(second)))
    return (bright + 0.05) / (dark + 0.05)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", type=rgb)
    parser.add_argument("background", type=rgb)
    parser.add_argument("--require", choices=("aa", "aa-large", "aaa", "aaa-large"))
    args = parser.parse_args()
    ratio = contrast(args.text, args.background)
    targets = {"aa": 4.5, "aa-large": 3.0, "aaa": 7.0, "aaa-large": 4.5}
    print(f"Contrast: {ratio:.2f}:1")
    for label, threshold in targets.items():
        print(f"{label.upper():<10} {'pass' if ratio >= threshold else 'fail'}")
    black = contrast((0, 0, 0), args.background)
    white = contrast((255, 255, 255), args.background)
    print(f"Higher-contrast text: {'#000000' if black >= white else '#FFFFFF'}")
    return 1 if args.require and ratio < targets[args.require] else 0


if __name__ == "__main__":
    raise SystemExit(main())
