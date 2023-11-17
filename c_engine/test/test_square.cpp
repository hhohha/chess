
#include "utest.h"
#include "square.h"

int main() {
    TestSuite unitTests;

    unitTests.addTest("test1", []() {
        Square s(4, nullptr);
        assertEqual(3, s.get_col());
    });

    unitTests.addTest("test2", []() {
        assertEqual(1 == 1, 2 == 3);
    });

    unitTests.addTest("test3", []() {
        assertEqual("str1", "str2");
    });

    unitTests.run();
}

