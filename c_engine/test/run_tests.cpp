#include <vector>

#include "utest.h"


TestSuite create_test_suite_squares();
TestSuite create_test_suite_moves();
TestSuite create_test_suite_bishop();
TestSuite create_test_suite_rook();
TestSuite create_test_suite_queen();
TestSuite create_test_suite_knight();
TestSuite create_test_suite_king();
TestSuite create_test_suite_pawn();
TestSuite create_test_suite_board();
TestSuite create_test_suite_tree_search();


int main(int argc, char **argv) {
    std::string suiteName;
    std::string testName;

    if (argc >  1)
        suiteName = argv[1];

    if (argc > 2)
        testName = argv[2];


    std::vector<TestSuite> testSuites;

    testSuites.emplace_back(create_test_suite_squares());
    testSuites.emplace_back(create_test_suite_moves());
    testSuites.emplace_back(create_test_suite_bishop());
    testSuites.emplace_back(create_test_suite_rook());
    testSuites.emplace_back(create_test_suite_queen());
    testSuites.emplace_back(create_test_suite_knight());
    testSuites.emplace_back(create_test_suite_king());
    testSuites.emplace_back(create_test_suite_pawn());
    testSuites.emplace_back(create_test_suite_board());
    testSuites.emplace_back(create_test_suite_tree_search());

    for (auto &testSuite: testSuites)
        if (suiteName.empty() || str_equal_ignore_case(testSuite.suiteName, suiteName))
            testSuite.run(testName);

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