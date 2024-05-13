

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <cstring>
#include "board.h"
#include "move.h"

std::string get_moves_str(Board &board) {
    std::string result;
    auto moves = board.get_legal_moves();
    for (auto move: moves) {
        result += move->str() + " ";
    }
    return result.substr(0, result.size() - 1);
}

std::string handle_message(const std::string &message, Board &board) {
    auto space = message.find(' ');
    std::string command, arg;

    if (space == std::string::npos) {
        command = message;
    } else {
        command = message.substr(0, space);
        arg = message.substr(space + 1);
    }

//    std::cout << "Command: " << command << " Arg: " << arg << std::endl;

    if (command == "clear") {
        board.clear();
        return "OK";
    } else if (command == "load_fen") {
        board.load_fen(arg);
        return get_moves_str(board);
    } else if (command == "get_legal_moves") {
        return get_moves_str(board);
    } else if (command == "perform_move") {
        auto move = board.create_move(arg);
        board.perform_move(move);
        board._legalMoves.push_back(board.calc_all_legal_moves());
        return get_moves_str(board);
    } else if (command == "undo_move") {
        board.undo_move();
        board._legalMoves.push_back(board.calc_all_legal_moves());
        return get_moves_str(board);
    } else if (command == "get_best_move") {
        auto best_move = board.get_best_move();
        return best_move.first.str();
    } else {
        return "Unknown command - " + command + " " + arg + "\n";
    }
}

int main(int argc, char **argv) {

    int port = 20002;
    char *end;
    if (argc > 1) {
        long temp = std::strtol(argv[1], &end, 10);
        if (*end || temp < 0 || temp > 65535) {
            std::cout << "Invalid port number. Using default port 20002." << std::endl;
        } else {
            port = temp;
            std::cout << "Using port " << port << std::endl;
        }
    }

    int client_fd, server_fd;
    ssize_t size;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addrlen = sizeof(server_addr);
    int opt = 1;
    const int BUFFER_SIZE = 2048;

    char buffer[BUFFER_SIZE] = { 0 };
    std::string response;

    Board board;

    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    if (server_fd < 0) {
        std::cout << "Error opening socket" << std::endl;
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cout << "Error binding socket" << std::endl;
        return 1;
    }

    if (listen(server_fd, 3) < 0) {
        std::cout << "Error listening on socket" << std::endl;
        return 1;
    }

    while (true) {
        int len = sizeof(client_addr);
//        std::cout << "Waiting for connection" << std::endl;
        if ((client_fd = accept(server_fd, (struct sockaddr *) &server_addr, (socklen_t *) &len)) < 0) {
            std::cout << "Error accepting connection" << std::endl;
            return 1;
        }

        char *client_ip = inet_ntoa(client_addr.sin_addr);
//        std::cout << "Connection from " << client_ip << ", " << ntohs(client_addr.sin_port) << std::endl;

        memset(buffer, 0, sizeof(buffer));

        size = read(client_fd, buffer, BUFFER_SIZE - 1);
        if (size < 0) {
            std::cout << "Error reading from socket" << std::endl;
            return 1;
        }

        std::string message(buffer);
        size_t endOfMsg = message.find_last_not_of(" \t\r\n");
        if (endOfMsg != std::string::npos) {
            message = message.substr(0, endOfMsg + 1);
        }

//        std::cout << "Received message: " << message << "\n" << std::endl;

        response = handle_message(message, board);


        if (write(client_fd, response.c_str(), response.size()) < 0) {
            std::cout << "Error writing to socket" << std::endl;
            return 1;
        }
        close(client_fd);
    }
    close(server_fd);
    return 0;
}
