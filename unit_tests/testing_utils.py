from typing import List
from move import Move


def compare_moves(actualMoves: List[Move], expectedMoves: List[str]) -> bool:
    return set(map(str, actualMoves)) == set(expectedMoves)