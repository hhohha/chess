#pragma once

#include <vector>

#include "move.h"

class Search_tree_node {
    int score;
    int depth;
    std::vector<Search_tree_node> children;
    Search_tree_node *parent;
    Move *move;
};

class Search_tree {
    Search_tree_node root;
};
