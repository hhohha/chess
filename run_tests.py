from __future__ import annotations
import os
import sys
import importlib.util


TEST_DIR = 'unit_tests'

RED_TEXT = ''
NORMAL_TEXT = ''
GREEN_TEXT = ''
YELLOW_TEXT = ''

COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_WHITE = '\x1b[0m'

vline = '-' * 158


class TestSummary:
    def __init__(self):
        self.all = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def update(self, other: TestSummary) -> None:
        self.all += other.all
        self.passed = other.passed
        self.failed = other.failed
        self.skipped = other.skipped

    def get_pass_rate(self) -> str:
        return f"{round(self.passed * 100 / self.all, 2)}%"

def print_test_result(item, desc, result, msg):
    desc = desc.strip()
    print(f'| {item:40} | {desc:100} |  {result:16} |')
    if msg:
        print(f'\n{COLOR_RED}\n{msg}\n{COLOR_WHITE}\n')


def run_test_suite(testClass, testSuiteName):
    print(vline)
    print(f'| TEST SUITE: {testSuiteName.removeprefix("TestSuite_"):142} |')
    print(vline)
    testObj = testClass()
    summary = TestSummary()

    for item in dir(testObj):
        # these classes must contain methods starting with "test_" - run all these methods
        if item.startswith("test_"):
            test = getattr(testObj, item)
            errDetails = ''
            try:
                test()
                testResult = f"{COLOR_GREEN}PASSED{COLOR_WHITE}"
                summary.passed += 1
            except AssertionError as e:
                testResult = f"{COLOR_RED}FAILED{COLOR_WHITE}"
                errDetails = str(e)
                summary.failed += 1
            summary.all += 1
            print_test_result(item, "" if not test or not test.__doc__ else test.__doc__, testResult, errDetails)

    print(vline)
    print(f"| PASSED TEST IN SUITE: {summary.passed:2} out of {summary.all:2}    FAILED: {summary.failed:2}   SKIPPED: {summary.skipped:2}   PASS RATE: {summary.get_pass_rate():6}{' '*73}|")
    print(vline)
    return summary



def main():
    if not len(sys.argv) > 1:
        print(f'no tests specified, running all tests in test directory {TEST_DIR}')
        testFiles = os.listdir(TEST_DIR)
    else:
        print(f'running tests {sys.argv[1:]}')
        testFiles = sys.argv[1:]

    for testFile in testFiles:

        # 1. import the file, the test file must be named "test_*.py"
        if not testFile.startswith("test_") or not testFile.endswith(".py"):
            testFile = f'test_{testFile}.py'

        try:
            spec = importlib.util.spec_from_file_location(testFile.removesuffix('.py'), f'{TEST_DIR}/{testFile}')
            module = importlib.util.module_from_spec(spec)
            sys.modules[testFile] = module
            spec.loader.exec_module(module)
        except FileNotFoundError:
            print(f'file {testFile} not found, skipping')
            continue

        # 2. the file must contain some classes starting with "TestSuite_" - instantiate all such classes
        testSuites = filter(lambda m: m.startswith('TestSuite_'), dir(module))

        for testSuiteName in testSuites:
            testSuite = getattr(module, testSuiteName)
            run_test_suite(testSuite, testSuiteName)


if __name__ == '__main__':
    main()