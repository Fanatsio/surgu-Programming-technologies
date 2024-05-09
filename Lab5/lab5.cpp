#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <sstream>
#include <bitset>

// Структура узла дерева Хаффмана
struct Node {
    int symbol;
    int frequency;
    Node* left;
    Node* right;

    Node(int sym, int freq) : symbol(sym), frequency(freq), left(nullptr), right(nullptr) {}
};

// Построение дерева Хаффмана (с использованием стабильной сортировки)
Node* buildHuffmanTree(const std::vector<int>& frequencies) {
    std::vector<Node*> nodes;
    for (int i = 0; i < frequencies.size(); ++i) {
        if (frequencies[i] > 0) {
            nodes.push_back(new Node(i, frequencies[i]));
        }
    }

    while (nodes.size() > 1) {
        std::stable_sort(nodes.begin(), nodes.end(), [](const Node* a, const Node* b) {
            return a->frequency < b->frequency;
        });

        Node* left = nodes.back();
        nodes.pop_back();
        Node* right = nodes.back();
        nodes.pop_back();

        Node* parent = new Node(-1, left->frequency + right->frequency);
        parent->left = left;
        parent->right = right;
        nodes.push_back(parent);
    }

    return nodes.front();
}

// Генерация кодов Хаффмана
void generateHuffmanCodes(Node* root, const std::string& code, std::map<int, std::string>& codes) {
    if (!root)
        return;

    if (root->symbol != -1) {
        codes[root->symbol] = code;
    }

    generateHuffmanCodes(root->left, code + "0", codes);
    generateHuffmanCodes(root->right, code + "1", codes);
}

// Функция для сжатия файла PPM
void compressPPM(const std::string& inputFileName, const std::string& outputFileName) {
    std::ifstream inputFile(inputFileName, std::ios::binary);
    std::ofstream outputFile(outputFileName, std::ios::binary);

    if (!inputFile.is_open() || !outputFile.is_open()) {
        std::cerr << "Error opening files!" << std::endl;
        return;
    }

    // Чтение заголовка PPM
    std::string magicNumber;
    int width, height, maxColorValue;
    inputFile >> magicNumber >> width >> height >> maxColorValue;
    outputFile << magicNumber << "\n" << width << " " << height << "\n" << maxColorValue << "\n";

    // Считаем частоту появления каждого цвета
    std::vector<int> frequencies(256, 0);
    char pixel;
    while (inputFile.get(pixel)) {
        frequencies[static_cast<unsigned char>(pixel)]++;
    }

    // Вывод частот символов в консоль
    std::cout << "Frequencies:" << std::endl;
    for (int i = 0; i < frequencies.size(); ++i) {
        if (frequencies[i] > 0) {
            std::cout << "Symbol: " << i << ", Frequency: " << frequencies[i] << std::endl;
        }
    }

    // Построение дерева и генерация кодов
    Node* huffmanTree = buildHuffmanTree(frequencies);
    std::map<int, std::string> huffmanCodes;
    generateHuffmanCodes(huffmanTree, "", huffmanCodes);

    // Запись кодов Хаффмана с разделителями
    for (auto& code : huffmanCodes) {
        outputFile << code.first << " " << code.second << "\n";
    }

    // Переходим к началу файла, чтобы сжимать данные
    inputFile.clear();
    inputFile.seekg(0, std::ios::beg);

    // Сжатие данных с учетом заполняющих нулей
    std::string buffer;
    int paddingBits = 0;
    while (inputFile.get(pixel)) {
        buffer += huffmanCodes[static_cast<unsigned char>(pixel)];
        while (buffer.length() >= 8) {
            std::bitset<8> bits(buffer.substr(0, 8));
            outputFile.put(static_cast<char>(bits.to_ulong()));
            buffer = buffer.substr(8);
        }
    }

    // Дописывание последнего байта и количества заполняющих нулей
    if (!buffer.empty()) {
        paddingBits = 8 - buffer.length();
        while (buffer.length() < 8) {
            buffer += "0";
        }
        std::bitset<8> bits(buffer);
        outputFile.put(static_cast<char>(bits.to_ulong()));
    }
    outputFile << paddingBits << "\n"; 

    // Освобождение памяти
    delete huffmanTree;

    inputFile.close();
    outputFile.close();
}

// Распаковка файла PPM (с чтением всей строки и учетом заполняющих нулей)
void decompressPPM(const std::string& inputFileName, const std::string& outputFileName) {
    std::ifstream inputFile(inputFileName, std::ios::binary);
    std::ofstream outputFile(outputFileName, std::ios::binary);

    if (!inputFile.is_open() || !outputFile.is_open()) {
        std::cerr << "Error opening files!" << std::endl;
        return;
    }

    // Чтение заголовка PPM
    std::string magicNumber;
    int width, height, maxColorValue;
    inputFile >> magicNumber >> width >> height >> maxColorValue;
    outputFile << magicNumber << "\n" << width << " " << height << "\n" << maxColorValue << "\n";

    // Чтение кодов Хаффмана с использованием std::getline
    std::map<int, std::string> huffmanCodes;
    std::string line;
    while (std::getline(inputFile, line)) { 
        std::istringstream iss(line);
        int symbol;
        std::string code;
        if (iss >> symbol >> code) {
            huffmanCodes[symbol] = code; 
        } 
    } 

    // Отладочный вывод: вывод кодов Хаффмана в консоль
    std::cout << "Huffman Codes:" << std::endl;
    for (const auto& entry : huffmanCodes) {
        std::cout << "Symbol: " << entry.first << ", Code: " << entry.second << std::endl;
    }

    // Распаковка данных с учетом заполняющих нулей
    Node* huffmanTree = buildHuffmanTree(std::vector<int>()); 
    Node* currentNode = huffmanTree; 
    char byte; 
    int paddingBits;
    inputFile >> paddingBits; // Чтение количества заполняющих нулей
    while (inputFile.get(byte)) { 
        std::bitset<8> bits(byte); 
        for (int i = 7; i >= 0; --i) { 
            if (bits[i] == 0) { 
                currentNode = currentNode->left; 
            } else { 
                currentNode = currentNode->right; 
            } 

            if (currentNode->left == nullptr && currentNode->right == nullptr) { 
                outputFile.put(static_cast<char>(currentNode->symbol)); 
                currentNode = huffmanTree; 
            } 
        } 
    } 

    // Освобождение памяти
    delete huffmanTree;

    inputFile.close();
    outputFile.close();
}

bool compareFiles(const std::string& file1, const std::string& file2) {
    std::ifstream f1(file1, std::ios::binary | std::ios::ate);
    std::ifstream f2(file2, std::ios::binary | std::ios::ate);

    if (f1.fail() || f2.fail()) {
        std::cerr << "Error opening files!" << std::endl;
        return false;
    }

    if (f1.tellg() != f2.tellg()) {
        return false;
    }

    f1.seekg(0, std::ios::beg);
    f2.seekg(0, std::ios::beg);

    std::vector<char> buffer1(std::istreambuf_iterator<char>(f1), {});
    std::vector<char> buffer2(std::istreambuf_iterator<char>(f2), {});

    return buffer1 == buffer2;
}

int main() {
    std::string originalFile = "input.ppm";
    std::string compressedFile = "compressed.ppm";
    std::string decompressedFile = "output.ppm";

    // Сжатие и распаковка файла
    compressPPM(originalFile, compressedFile);
    decompressPPM(compressedFile, decompressedFile);

    // Сравнение исходного файла и файла после сжатия и распаковки
    if (compareFiles(originalFile, decompressedFile)) {
        std::cout << "Files are identical." << std::endl;
    } else {
        std::cout << "Files are different." << std::endl;
    }

    return 0;
}
