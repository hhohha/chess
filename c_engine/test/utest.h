#include <iostream>
#include <string>
#include <vector>

using testFuncPtr = void (*)(void);

template<typename T>
void assertEqual(T expected, T actual) {
    if (expected != actual) {
        throw std::runtime_error("Expected " + std::to_string(expected) + " but got " + std::to_string(actual));
    }
}

template<>
inline void assertEqual<const char*>(const char* expected, const char* actual) {
    if (expected != actual) {
        throw std::runtime_error("Expected \"" + std::string(expected) + "\" but got \"" + std::string(actual) + "\"");
    }
}

class TestSuite {
public:
    TestSuite() {
    }

    void addTest(std::string name, testFuncPtr func) {
        tests.emplace_back(name, func);
    }

    void run() {
        for (auto test: tests)
            try {
                test.func();
                std::cout << "Test " << test.name << " passed" << std::endl;
            } catch (std::runtime_error &e) {
                std::cout << "Test " << test.name << " failed: " << e.what() << std::endl;
            }
    }

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
