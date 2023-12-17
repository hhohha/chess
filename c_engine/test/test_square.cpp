
#include "utest.h"
#include "square.h"

TestSuite create_test_suite_squares() {
    TestSuite testSuite("Squares");

    testSuite.add_test("Square construction", []() {
        {
            Square s;
            s.init(0, nullptr);

            assert_equal(0, s.get_col());
            assert_equal(0, s.get_row());
            assert_equal("a1", s.get_name());
            assert_true(s.is_free());
            assert_false(s.is_attacked_by(Color::WHITE));
            assert_false(s.is_attacked_by(Color::BLACK));
        }
        {
            Square s;
            s.init(63, nullptr);

            assert_equal(7, s.get_col());
            assert_equal(7, s.get_row());
            assert_equal("h8", s.get_name());
        }
        {
            Square s;
            s.init(56, nullptr);

            assert_equal(0, s.get_col());
            assert_equal(7, s.get_row());
            assert_equal("a8", s.get_name());
        }
        {
            Square s;
            s.init(7, nullptr);

            assert_equal(7, s.get_col());
            assert_equal(0, s.get_row());
            assert_equal("h1", s.get_name());
        }
    });

    testSuite.add_test("Square comparison", []() {
        Square s1;
        s1.init(0, nullptr);
        Square s2;
        s2.init(0, nullptr);
        Square s3;
        s3.init(1, nullptr);

        assert_true(s1 == s2);
        assert_false(s1 != s2);
        assert_true(s1 != s3);
        assert_false(s1 == s3);
    });

    return testSuite;
}