
#include "utest.h"
#include "square.h"

TestSuite create_test_suite_squares() {
    TestSuite testSuite("Squares");

    testSuite.addTest("Square construction", []() {
        Square s(0, nullptr);

        assertEqual(0, s.get_col());
        assertEqual(0, s.get_row());
        assertEqual("a1", s.get_name());
        assertTrue(s.is_free());
        assertFalse(s.is_attacked_by(Color::WHITE));
        assertFalse(s.is_attacked_by(Color::BLACK));

        s = Square(63, nullptr);
        assertEqual(7, s.get_col());
        assertEqual(7, s.get_row());
        assertEqual("h8", s.get_name());

        s = Square(56, nullptr);
        assertEqual(0, s.get_col());
        assertEqual(7, s.get_row());
        assertEqual("a8", s.get_name());

        s = Square(7, nullptr);
        assertEqual(7, s.get_col());
        assertEqual(0, s.get_row());
        assertEqual("h1", s.get_name());
    });

    testSuite.addTest("Square comparison", []() {
        Square s1(0, nullptr);
        Square s2(0, nullptr);
        Square s3(1, nullptr);

        assertTrue(s1 == s2);
        assertFalse(s1 != s2);
        assertTrue(s1 != s3);
        assertFalse(s1 == s3);
    });

    return testSuite;
}