
#include "utest.h"
#include "square.h"

void test_square_creation() {
    Square s(0, nullptr);
    assertEqual(0, s.get_col());
}

void test_square_creation2() {
    Square s(1, nullptr);
    assertEqual(1, s.get_col());
}

void test_square_creation3() {
    Square s(2, nullptr);
    assertEqual(3, s.get_col());
}

int main() {
    TestSuite unitTests;
    unitTests.addTest("test1", test_square_creation);
    unitTests.addTest("test2", test_square_creation2);
    unitTests.addTest("test3", test_square_creation3);

    unitTests.addTest("test5", []() {
        Square s(4, nullptr);
        assertEqual(3, s.get_col());
    });

    unitTests.run();
}

