#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using testFuncPtr = void (*)(void);

inline bool str_equal_ignore_case(std::string str1, std::string str2) {
    if (str1.size() != str2.size())
        return false;

    for (unsigned int i = 0; i < str1.size(); ++i) {
        if (tolower(str1[i]) != tolower(str2[i]))
            return false;
    }

    return true;
}

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
inline void assertVectorContain(std::vector<T *> &vector, const char* itemStr) {
    for (auto m : vector) {
        if (m->str() == itemStr)
            return;
    }

    throw std::runtime_error("Expected vector to contain " + std::string(itemStr));
}

template<typename T>
inline void assertVectorContain(const std::vector<T> &vector, T item) {
    for (auto item2 : vector) {
        if (item == item2)
            return;
    }

    std::stringstream ss;
    ss << "Expected vector to contain " << item;

    throw std::runtime_error(ss.str());
}

inline void assertIsNull(void *ptr, std::string msg = "") {
    if (ptr != nullptr) {
        throw std::runtime_error("Expected pointer to be null" + (msg.empty() ? "" : ": " + msg));
    }
}

inline void assertTrue(bool expression, std::string msg = "") {
    if (!expression) {
        throw std::runtime_error("Expected expression to be true" + (msg.empty() ? "" : ": " + msg));
    }
}

inline void assertFalse(bool expression, std::string msg = "") {
    if (expression) {
        throw std::runtime_error("Expected expression to be false" + (msg.empty() ? "" : ": " + msg));
    }
}

class TestSuite {
public:
    TestSuite(std::string suiteName) : suiteName(suiteName) {}
    void addTest(std::string name, testFuncPtr func) {
        tests.emplace_back(name, func);
    }

    void run(std::string testName) {
        std::cout << std::endl;
        std::cout << "==========================================" << std::endl;
        std::cout << "Running test suite " << suiteName << std::endl;
        std::cout << "==========================================" << std::endl;
        std::cout << std::endl;

        for (auto test: tests)
            if (testName.empty() || str_equal_ignore_case(test.name, testName)) {
                try {
                    test.func();
                    std::cout << "Test " << test.name << ": \033[92m PASSED \x1b[0m  " << std::endl;
                    ++passed;
                } catch (std::runtime_error &e) {
                    std::cout << "Test " << test.name << ": \033[91m FAILED \x1b[0m  " << e.what() << std::endl;
                    ++failed;
                } 
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
