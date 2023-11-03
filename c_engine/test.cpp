#include <vector>
#include <iterator>
#include <iostream>

class Matrix {
public:
    std::vector<int>::iterator getIterToAllVectors() {
        std::vector<std::vector<int> *> v = {&v1, &v2, &v3, &v4, &v5};
        std::vector<std::vector<int> *>::iterator iter = v.begin();
        std::vector<int>::iterator iter2 = (*iter)->begin();
        return iter2;
    }

    std::vector<int> v1 = {11, 12, 13, 14, 15};
    std::vector<int> v2 = {21, 22, 23, 24, 25};
    std::vector<int> v3 = {31, 32, 33, 34, 35};
    std::vector<int> v4 = {41, 42, 43, 44, 45};
    std::vector<int> v5 = {51, 52, 53, 54, 55};

    //https://www.internalpointers.com/post/writing-custom-iterators-modern-cpp
};

int main() {
    Matrix m;

    auto iter = m.getIterToAllVectors();
    

}

