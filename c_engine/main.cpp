

#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include "board.h"
#include "move.h"

std::string handle_message(const char *message, Board &board) {
    std::string s(message);
    auto space = s.find(' ');
    std::string command, arg;

    if (space == std::string::npos) {
        command = s;
    } else {
        command = s.substr(0, space);
        arg = s.substr(space + 1);
    }

    if (command == "clear") {
        board.clear();
        return "OK";
    } else if (command == "load_fen") {
        board.load_fen(arg);
        return "OK";
    } else if (command == "get_legal_moves") {
        std::string result;
        auto moves = board.get_legal_moves();
        for (auto move: moves) {
            result += move->str() + " ";
        }
        return result;
    } else {
        return "Unknown command";
    }

}

int main() {
    int new_socket, server_fd;
    ssize_t valread;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
    int opt = 1;
    int port = 8080;
    char buffer[1024] = { 0 };
    std::string response;

    Board board;

    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    if (server_fd < 0) {
        std::cout << "Error opening socket" << std::endl;
        return 1;
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        std::cout << "Error setting socket options" << std::endl;
        return 1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        std::cout << "Error binding socket" << std::endl;
        return 1;
    }

    if (listen(server_fd, 3) < 0) {
        std::cout << "Error listening on socket" << std::endl;
        return 1;
    }

    int cnt = 0;
    while (cnt < 5) {
        if ((new_socket = accept(server_fd, (struct sockaddr *) &address, (socklen_t *) &addrlen)) < 0) {
            std::cout << "Error accepting connection" << std::endl;
            return 1;
        }

        valread = read(new_socket, buffer, 1024 - 1);

        response = handle_message(buffer, board);

        send(new_socket, response.c_str(), response.length(), 0);
        cnt++;
    }

    return 0;
}
