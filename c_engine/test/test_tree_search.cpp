#include "board.h"
#include "constants.h"
#include "utest.h"
#include <chrono>

static long int totalTime = 0;
static long int totalNodes = 0;

TestSuite create_test_suite_tree_search() {
    class Position {
    public:
        int id;
        std::string name;
        std::string fen;
        std::vector<long int> refResults;

        void run_test(int depth) {
            Board b;
            b.load_fen(fen);

            std::cout << "Testing position " << id << " to depth " << depth << " -   ";

            auto start = std::chrono::high_resolution_clock::now();
            long int result = b.test_move_generation(depth);
            auto end = std::chrono::high_resolution_clock::now(); // Stop measuring time
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

            if (result == refResults[depth])
                std::cout << "OK:    " << result;
            else
                std::cout << "FAILED:    "  << result << "   expected: " << refResults[depth];

            std::cout << "         time taken: " << (double)duration / 1000000 << " sec" << std::endl;
            totalTime += duration;
            totalNodes += result;
        }
    };


    TestSuite testSuite("Tree search");

    testSuite.add_test("Tree search", []() {
        Board b;
        std::vector<Position> positions;                         //      1     2      3         4          5           6
        positions.push_back({1, "Position 1", FEN_INIT,             {1, 20,  400,  8902,   197281,   4865609,  119060324}});
        positions.push_back({2, "Position 2", FEN_TEST_A,           {1,  3,   21,   108,     1249,      6221,      91995}});
        positions.push_back({3, "Position 3", FEN_TEST_B,           {1, 44, 1486, 62379,  2103487,  89941194, 3048196529}});
        positions.push_back({4, "Position 4", FEN_TEST_C,           {1, 14,  191,  2812,    43238,    674624,   11030083}});
        positions.push_back({5, "Position 5", FEN_TEST_D,           {1,  6,  264,  9467,   422333,  15833292,  706045033}});
        positions.push_back({6, "Position 6", FEN_TEST_D_INVERTED,  {1,  6,  264,  9467,   422333,  15833292,  706045033}});
        positions.push_back({7, "Position 7", FEN_TEST_E,           {1, 48, 2039, 97862,  4085603, 193690690, 8031647685}});
        positions.push_back({8, "Position 8", FEN_TEST_E_NO_CASTLE, {1, 46, 1866, 86677,  3504849, 161724713, 6554868204}});
        positions.push_back({9, "Position 9", FEN_TEST_F,           {1, 46, 2079, 89890,  3894594, 164075551, 6923051137}});

        for (auto &position: positions)
            for (int depth = 4; depth <= 4; depth++) {
                position.run_test(depth);
        }

        std::cout << "Total time taken: " << (double)totalTime / 1000000  << " sec" << std::endl;
        std::cout << "Total nodes generated: " << totalNodes  << std::endl;
        std::cout << "Nodes per second: " << (double)totalNodes / totalTime * 1000000 << std::endl;
    });

    return testSuite;
}