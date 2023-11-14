#include <vector>
#include <iterator>
#include <iostream>

class PieceIterator;
class Matrix;

///////////////////   pieces definitions ///////////////////////

struct Piece {
    Piece(int v) : _value(v) {}     // constructor
    virtual std::string which_piece() = 0;    // identifier
    
    int _value;
};

struct Pawn : public Piece {
    Pawn(int v): Piece(v) {}
    std::string which_piece() override { return "Pawn"; }
};

struct Knight : public Piece {
    Knight(int v): Piece(v) {}
    std::string which_piece() override { return "Knight"; }
};

struct Bishop : public Piece {
    Bishop(int v): Piece(v) {}
    std::string which_piece() override { return "Bishop"; }
};

struct Rook : public Piece {
    Rook(int v): Piece(v) {}
    std::string which_piece() override { return "Rook"; }
};

struct Queen : public Piece {
    Queen(int v): Piece(v) {}
    std::string which_piece() override { return "Queen"; }
};

struct King : public Piece {
    King(int v): Piece(v) {}
    std::string which_piece() override { return "King"; }
};

/////////////// iterator header ///////////////////////

struct PieceIterator {
    using iterator_category = std::input_iterator_tag;
    using difference_type   = std::ptrdiff_t;
    using value_type        = Piece;
    using pointer           = Piece*;
    using reference         = Piece&;

    PieceIterator(Matrix *m, BaseCls *ptr = nullptr);

    reference operator*() const;
    pointer operator->();

    PieceIterator& operator++();
    PieceIterator operator++(int);

    bool operator== (const PieceIterator &other);
    bool operator!= (const PieceIterator &other);

    Matrix *_matrix;
    BaseCls *_ptr;
};

///////////////////// board header /////////////////////////

struct Board {
    PieceIterator begin();
    PieceIterator end();

    std::vector<Pawn> pawns = {11, 12, 13, 14, 15};
    std::vector<Knight> knights = {21, 22};
    std::vector<Bishop> bishops = {31, 32};
    std::vector<Rook> rooks = {41, 42};
    std::vector<Queen> queens = {51};
    std::vector<King> kings = {61};

};

////////////////////// iterator functions ///////////////////////

PieceIterator::PieceIterator(Board *m, BaseCls *ptr) : _matrix(m), _ptr(ptr == nullptr ? &m->v1[0] : ptr) {}
BaseCls &PieceIterator::operator*() const { return *_ptr; }
BaseCls *PieceIterator::operator->() { return _ptr; }

PieceIterator& PieceIterator::operator++() {
    if (_ptr == &_matrix->v1[4])
        _ptr = &_matrix->v2[0];
    else
        ++_ptr;

    return *this;
}

PieceIterator PieceIterator::operator++(int) { PieceIterator tmp = *this; ++(*this); return tmp; }

bool PieceIterator::operator== (const PieceIterator &other) { return this->_ptr == other._ptr; }
bool PieceIterator::operator!= (const PieceIterator &other) { return this->_ptr != other._ptr; }

////////////////////// board functions ///////////////////////

PieceIterator Board::begin() { return PieceIterator(this); }
PieceIterator Board::end()   { return PieceIterator(this, &v2[5]); }

////////////////////// main //////////////////////////////////

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

int mainx() {
    Matrix m;

    for (PieceIterator it(&m); it != m.end(); ++it)
        std::cout << it->_value << std::endl;

    // std::vector<int> v1 = {1, 2, 3, 4};

    // std::cout << "before:\nv1: " << vector_to_string(v1) << "    addr: " << &v1 << std::endl;

    // std::vector<int> &v2 = change_and_return(v1);
    
    // std::cout << "\nafter:\nv1: " <<  vector_to_string(v1) << "    addr: " << &v1 << std::endl;
    // std::cout << "v2: " <<  vector_to_string(v2) << "    addr: " << &v2 << std::endl;

    return 0;

}

