#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using testFuncPtr = void (*)(void);

template<typename T1, typename T2>
inline void assertEqual(T1 expected, T2 actual) {
    if (expected != actual) {
        std::stringstream ss;
        ss << "Expected " << expected << " but got " << actual;
        //throw std::runtime_error("Expected " + std::to_string(expected) + " but got " + std::to_string(actual));
        throw std::runtime_error(ss.str());
    }
}

template<typename T1, typename T2>
inline void assertEqual(T1 *expected, T2 *actual) {
    if (expected != actual) {
        std::stringstream ss;
        ss << "Expected " << *expected << " but got " << *actual;
        //throw std::runtime_error("Expected " + std::to_string(expected) + " but got " + std::to_string(actual));
        throw std::runtime_error(ss.str());
    }
}

template<typename T>
inline void assertVectorContain(std::vector<T *> &vec, const char* s) {
    for (auto m : vec) {
        if (m->str() == s)
            return;
    }

    throw std::runtime_error("Expected voctor to contain " + std::string(s));
}
/*
template<>
inline void assertEqual<const char*, std::string>(const char* expected, std::string actual) {
    if (expected != actual) {
        throw std::runtime_error("Expected \"" + std::string(expected) + "\" but got \"" + actual + "\"");
    }
}*/

inline void assertIsNull(void *ptr) {
    if (ptr != nullptr) {
        throw std::runtime_error("Expected pointer to be null");
    }
}

inline void assertTrue(bool expression) {
    if (!expression) {
        throw std::runtime_error("Expected expression to be true");
    }
}

inline void assertFalse(bool expression) {
    if (expression) {
        throw std::runtime_error("Expected expression to be false");
    }
}

class TestSuite {
public:
    TestSuite(std::string suiteName) : suiteName(suiteName) {}
    void addTest(std::string name, testFuncPtr func) {
        tests.emplace_back(name, func);
    }

    void run() {
        std::cout << std::endl;
        std::cout << "==========================================" << std::endl;
        std::cout << "Running test suite " << suiteName << std::endl;
        std::cout << "==========================================" << std::endl;
        std::cout << std::endl;

        for (auto test: tests)
            try {
                test.func();
                std::cout << "Test " << test.name << ": \033[92m PASSED \x1b[0m  " << std::endl;
                ++passed;
            } catch (std::runtime_error &e) {
                std::cout << "Test " << test.name << ": \033[91m FAILED \x1b[0m  " << e.what() << std::endl;
                ++failed;
            }

        std::cout << std::endl;
        std::cout << "Passed tests: " << passed << std::endl;
        std::cout << "Failed tests: " << failed << std::endl;
        std::cout << "Skipped tests: " << skipped << std::endl;
    }

    std::string suiteName;
    unsigned int passed = 0;
    unsigned int failed = 0;
    unsigned int skipped = 0;
    

private:
    class UnitTest {
    public:
        UnitTest(std::string name, testFuncPtr func)
            :name(name), func(func) {
        }


    private:
        std::string name;
        testFuncPtr func;

        friend class TestSuite;
    };

    std::vector<UnitTest> tests;
};
