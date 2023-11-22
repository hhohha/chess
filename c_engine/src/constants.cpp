#include "constants.h"

std::ostream &operator<<(std::ostream &os, const PieceType &pieceType) {
    switch (pieceType) {
        case PieceType::PAWN:
            os << "pawn";
            break;
        case PieceType::KNIGHT:
            os << "knight";
            break;
        case PieceType::BISHOP:
            os << "bishop";
            break;
        case PieceType::ROOK:
            os << "rook";
            break;
        case PieceType::QUEEN:
            os << "queen";
            break;
        case PieceType::KING:
            os << "king";
            break;
    }
    return os;
}

std::ostream &operator<<(std::ostream &os, const Color &color) {
    switch (color) {
        case Color::WHITE:
            os << "white";
            break;
        case Color::BLACK:
            os << "black";
            break;
    }
    return os;
}

std::ostream &operator<<(std::ostream &os, const Direction &direction) {
    switch (direction) {
        case Direction::DOWN:
            os << "down";
            break;
        case Direction::UP:
            os << "up";
            break;
        case Direction::RIGHT:
            os << "right";
            break;
        case Direction::LEFT:
            os << "left";
            break;
        case Direction::DOWN_RIGHT:
            os << "down right";
            break;
        case Direction::DOWN_LEFT:
            os << "down left";
            break;
        case Direction::UP_RIGHT:
            os << "up right";
            break;
        case Direction::UP_LEFT:
            os << "up left";
            break;
    }
    return os;
}