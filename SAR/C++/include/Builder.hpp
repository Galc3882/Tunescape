#ifndef BUILDER_HPP
#define BUILDER_HPP

#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include <opencv2/opencv.hpp>

class Builder
{
public:
    static std::tuple<std::string, std::string, double, int, int, double, double, int, int, int, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<int>, std::vector<int>, std::vector<int>, std::vector<int>> getFeatures(const std::string &hdf5_file);
    static void processChunk(const std::string &root, int chunkSize);
};

#endif // BUILDER_HPP
