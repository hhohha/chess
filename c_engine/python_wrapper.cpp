#include <pybind11/pybind11.h>

#include "board.h"

PYBIND11_MODULE(libdboard, m) {
    pybind11::class_<Board>(m, "Board")
        .def(pybind11::init<>())
        .def("load_fen", &Board::load_fen)
        .def("make_move", &Board::make_move)
        .def("undo_move", &Board::undo_move)
        .def("get_legal_moves", &Board::get_legal_moves_str)
        .def("tprint", &Board::tprint);
}