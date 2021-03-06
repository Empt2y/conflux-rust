#!/usr/bin/env python3
import subprocess
import os
import sys

try:
    # Make sure python thinks it can write unicode to its stdout
    "\u2713".encode("utf_8").decode(sys.stdout.encoding)
    TICK = "✓ "
    CROSS = "✖ "
    CIRCLE = "○ "
except UnicodeDecodeError:
    TICK = "P "
    CROSS = "x "
    CIRCLE = "o "

BOLD, BLUE, RED, GREY = ("", ""), ("", ""), ("", ""), ("", "")
if os.name == 'posix':
    # primitive formatting on supported
    # terminal via ANSI escape sequences:
    BOLD = ('\033[0m', '\033[1m')
    BLUE = ('\033[0m', '\033[0;34m')
    RED = ('\033[0m', '\033[0;31m')
    GREY = ('\033[0m', '\033[1;30m')

TEST_SCRIPTS = []

test_dir = os.path.dirname(os.path.realpath(__file__))

# By default, run all *_test.py files in the same folder of this file.
for file in os.listdir(test_dir):
    if file.endswith("_test.py"):
        TEST_SCRIPTS.append(file)

failed = set()
for script in TEST_SCRIPTS:
    print("Running " + script, end = "\r")
    color = BLUE
    glyph = TICK
    try:
        py = "python3"

        if hasattr(sys, "getwindowsversion"):
            py = "python"

        subprocess.check_output(args = [py, script, "--randomseed=1"], stdin = None, cwd = test_dir)
    except subprocess.CalledProcessError as err:
        color = RED
        glyph = CROSS
        print("Output of " + script)
        print(err.output.decode("utf-8"))
        failed.add(script)
    print(color[1] + glyph + " Testcase " + script + color[0])

if len(failed) > 0:
    print("The following test fails: ")
    for c in failed:
        print(c)
    sys.exit(1)
