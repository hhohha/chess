import os
import sys
import importlib.util


TEST_DIR = 'unit_tests'

def run_test(testClass):
    testObj = testClass()
    for item in dir(testObj):
        if item.startswith("test_"):
            test = getattr(testObj, item)
            print(item, test())

def main():
    if not len(sys.argv) > 1:
        print(f'no tests specified, running all tests in test directory {TEST_DIR}')
        testFiles = os.listdir(TEST_DIR)
    else:
        print(f'running tests {sys.argv[1:]}')
        testFiles = sys.argv[1:]

    for testFile in testFiles:
        # 1. import the file, the test file must be named "test_*.py"
        if not testFile.startswith("test_") or not testFile.endswith("*.py"):
            continue

        spec = importlib.util.spec_from_file_location(testFile.removesuffix('.py'), f'{TEST_DIR}/{testFile}')
        module = importlib.util.module_from_spec(spec)
        sys.modules[testFile] = module
        spec.loader.exec_module(module)

        # 2. the file must contain some classes starting with "TestSuite_" - instantiate all such classes


        # 3. these classes must contain methods starting with "test_" - run all these methods
        # 4. see if they throw an assert exception (FAILED test) or not (PASSED test)

        pass

if __name__ == '__main__':
    main()