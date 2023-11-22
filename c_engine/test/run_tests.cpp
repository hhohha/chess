#include <vector>

#include "utest.h"


TestSuite create_test_suite_squares();
TestSuite create_test_suite_moves();
TestSuite create_test_suite_bishop();


int main() {
    std::vector<TestSuite> testSuites;

    testSuites.emplace_back(create_test_suite_squares());
    testSuites.emplace_back(create_test_suite_moves());
    testSuites.emplace_back(create_test_suite_bishop());

    for (auto &testSuite: testSuites)
        testSuite.run();

    unsigned int passed = 0;
    unsigned int failed = 0;
    unsigned int skipped = 0;

    for (auto &testSuite: testSuites) {
        passed += testSuite.passed;
        failed += testSuite.failed;
        skipped += testSuite.skipped;
    }

    std::cout << std::endl;
    std::cout << "==========================================" << std::endl;
    std::cout << "All test suites finished" << std::endl;
    std::cout << "Passed tests: " << passed << std::endl;
    std::cout << "Failed tests: " << failed << std::endl;
    std::cout << "Skipped tests: " << skipped << std::endl;
    std::cout << "==========================================" << std::endl;
}