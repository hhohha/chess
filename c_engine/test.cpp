#include <vector>
#include <iterator>
#include <iostream>

class MatrixIterator;
class Matrix;

struct BaseCls {
    BaseCls(int v) : _value(v) {}
    int _value;
};

struct DerivedCls1 : public BaseCls {
    DerivedCls1(int v): BaseCls(v) {
    }
};

struct DerivedCls2 : public BaseCls {
    DerivedCls2(int v): BaseCls(v) {
    }
};


struct MatrixIterator {
    using iterator_category = std::input_iterator_tag;
    using difference_type   = std::ptrdiff_t;
    using value_type        = BaseCls;
    using pointer           = BaseCls*;
    using reference         = BaseCls&;

    MatrixIterator(Matrix *m, BaseCls *ptr = nullptr);

    reference operator*() const;
    pointer operator->();

    MatrixIterator& operator++();
    MatrixIterator operator++(int);

    bool operator== (const MatrixIterator &other);
    bool operator!= (const MatrixIterator &other);

    Matrix *_matrix;
    BaseCls *_ptr;
};

struct Matrix {
    MatrixIterator begin();
    MatrixIterator end();

    std::vector<DerivedCls1> v1 = {11, 12, 13, 14, 15};
    std::vector<DerivedCls2> v2 = {21, 22, 23, 24, 25};
};


MatrixIterator Matrix::begin() { return MatrixIterator(this); }
MatrixIterator Matrix::end()   { return MatrixIterator(this, &v2[5]); }

MatrixIterator::MatrixIterator(Matrix *m, BaseCls *ptr) : _matrix(m), _ptr(ptr == nullptr ? &m->v1[0] : ptr) {}
BaseCls &MatrixIterator::operator*() const { return *_ptr; }
BaseCls *MatrixIterator::operator->() { return _ptr; }

MatrixIterator& MatrixIterator::operator++() {
    if (_ptr == &_matrix->v1[4])
        _ptr = &_matrix->v2[0];
    else
        ++_ptr;

    return *this;
}

MatrixIterator MatrixIterator::operator++(int) { MatrixIterator tmp = *this; ++(*this); return tmp; }

bool MatrixIterator::operator== (const MatrixIterator &other) { return this->_ptr == other._ptr; }
bool MatrixIterator::operator!= (const MatrixIterator &other) { return this->_ptr != other._ptr; }


std::vector<int> &change_and_return(std::vector<int> &v) {
    v[0] = 100;
    return v;
}

std::string vector_to_string(std::vector<int> v) {
    std::string s = "";
    for (auto i : v)
        s += std::to_string(i) + ", ";
    return s;
}

int main() {
    Matrix m;

    for (MatrixIterator it(&m); it != m.end(); ++it)
        std::cout << it->_value << std::endl;

    // std::vector<int> v1 = {1, 2, 3, 4};

    // std::cout << "before:\nv1: " << vector_to_string(v1) << "    addr: " << &v1 << std::endl;

    // std::vector<int> &v2 = change_and_return(v1);
    
    // std::cout << "\nafter:\nv1: " <<  vector_to_string(v1) << "    addr: " << &v1 << std::endl;
    // std::cout << "v2: " <<  vector_to_string(v2) << "    addr: " << &v2 << std::endl;

    return 0;

}

