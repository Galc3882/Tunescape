#include "debug.hpp"
#include "Search.hpp"
#include "FeatureSimilarity.hpp"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <thread>
#include <queue>
#include <random>
#include <fstream>
#include <stdexcept>
#include <ctime>
#include <cstdlib>

namespace Debug
{

    void main(const std::vector<float> &songValue, const std::vector<std::string> &pathList)
    {
        // Find most similar song using cosine similarity
        int numOfSongs = 5;
        std::vector<std::pair<std::string, float>> similarSongs = Search::multiProcessing(
            Search::findSimilarSongs, 32, songValue, pathList, numOfSongs);

        // Sort the list by the similarity score
        std::sort(similarSongs.begin(), similarSongs.end(), Search::takeSecond);
        if (similarSongs.size() > static_cast<size_t>(numOfSongs))
        {
            similarSongs.resize(numOfSongs);
        }

        std::cout << "Similar Songs: " << std::endl;
        for (const auto &song : similarSongs)
        {
            std::vector<std::string> songParts;
            split(song.first, '\0', songParts);
            std::cout << "Found Song: " << songParts[0] << " by " << songParts[1] << std::endl;
            std::cout << "Cosine Similarity: " << song.second << std::endl;
        }
    }

    void performanceTest()
    {
        // Ask for the song title
        std::string songTitle;
        std::cout << "Enter the song title: ";
        std::cin >> songTitle;

        // Find the song in the database
        std::string songKey = Search::fuzzyGetSongTitle(songTitle, std::string(os::getcwd()) + r '\tmp\namelist.pickle', 40);

        if (songKey.size() > 1)
        {
            std::cout << "Multiple songs found:" << std::endl;
            for (size_t j = 0; j < songKey.size(); j++)
            {
                std::vector<std::string> songParts;
                split(songKey[j], '\0', songParts);
                std::cout << j + 1 << ". " << songParts[0] << " by " << songParts[1] << std::endl;
            }
            std::cout << "Please enter the number of the song you want to use: ";
            int k;
            std::cin >> k;
            songKey = songKey[k - 1];
        }
        else
        {
            songKey = songKey[0];
        }

        std::vector<std::string> pathList;
        std::string root = std::string(os::getcwd()) + r '\tmp';
        for (const auto &path : os::walk(root))
        {
            for (const auto &name : path[2])
            {
                if (!startsWith(name, "namelist"))
                {
                    pathList.push_back(os::path.join(path[0], name));
                }
            }
        }

        std::vector<float> songValue;
        // Find song value in the database
        for (const auto &path : pathList)
        {
            std::ifstream file(path, std::ios::binary);
            if (file)
            {
                std::unordered_map<std::string, std::vector<float>> data;
                pickle::load(file, data);
                file.close();
                if (data.find(songKey) != data.end())
                {
                    songValue = data[songKey];
                    break;
                }
            }
        }

        if (songValue.empty())
        {
            // Error: Song not found
            return;
        }

        // Timing the main function
        std::clock_t start = std::clock();
        main(songValue, pathList);
        std::clock_t end = std::clock();
        double elapsed_time = double(end - start) / CLOCKS_PER_SEC;
        std::cout << "Time elapsed: " << elapsed_time << " seconds" << std::endl;
    }

    void printValues(const std::vector<float> &values)
    {
        std::cout << "Song: " << values[0] << std::endl;
        std::cout << "Band: " << values[1] << std::endl;
        std::cout << "Duration: " << values[2] << std::endl;
        std::cout << "Key: " << values[3] << std::endl;
        std::cout << "Mode: " << values[4] << std::endl;
        std::cout << "Speed: " << values[5] << std::endl;
        std::cout << "Loudness: " << values[6] << std::endl;
        std::cout << "Time signature: " << values[7] << std::endl;
        std::cout << "Year: " << values[8] << std::endl;
        std::cout << std::endl;
    }

    void compareValues(const std::vector<float> &values1, const std::vector<float> &values2)
    {
        std::cout << "Same artist: " << FeatureSimilarity::methodDictionary[1](values1[1], values2[1]) << std::endl;
        std::cout << "Duration similarity: " << FeatureSimilarity::methodDictionary[2](values1[2], values2[2]) << std::endl;
        std::cout << "Key similarity: " << FeatureSimilarity::methodDictionary[3](values1[3], values2[3], values1[4], values2[4]) << std::endl;
        std::cout << "Speed similarity: " << FeatureSimilarity::methodDictionary[5](values1[5], values2[5], values1[7], values2[7]) << std::endl;
        std::cout << "Loudness similarity: " << FeatureSimilarity::methodDictionary[6](values1[6], values2[6]) << std::endl;
        std::cout << "Year similarity: " << FeatureSimilarity::methodDictionary[8](values1[8], values2[8]) << std::endl;
        std::cout << "Sections start similarity: " << FeatureSimilarity::methodDictionary[9](values1[9], values2[9]) << std::endl;
        std::cout << "Segments pitches similarity: " << FeatureSimilarity::methodDictionary[10](values1[10], values2[10]) << std::endl;
        std::cout << "Segments timbre similarity: " << FeatureSimilarity::methodDictionary[11](values1[11], values2[11]) << std::endl;
        std::cout << "Bars start similarity: " << FeatureSimilarity::methodDictionary[12](values1[12], values2[12]) << std::endl;
        std::cout << "Beats start similarity: " << FeatureSimilarity::methodDictionary[13](values1[13], values2[13]) << std::endl;
        std::cout << "Tatums start similarity: " << FeatureSimilarity::methodDictionary[14](values1[14], values2[14]) << std::endl;
        std::cout << std::endl;
        std::cout << "Overall similarity: " << Search::cosineSimilarity(values1, values2) << std::endl;
        std::cout << std::endl;
    }

    void compareSongs(const std::vector<float> &values1, const std::vector<float> &values2)
    {
        // Assuming values1[10] and values2[10] are 2D arrays (images) represented as vectors of floats
        cv::Mat image1(values1[10].size(), values1[10][0].size(), CV_32FC1);
        cv::Mat image2(values2[10].size(), values2[10][0].size(), CV_32FC1);

        // Copy data from values1[10] and values2[10] to OpenCV Mats
        for (int i = 0; i < image1.rows; ++i)
        {
            for (int j = 0; j < image1.cols; ++j)
            {
                image1.at<float>(i, j) = values1[10][i][j];
                image2.at<float>(i, j) = values2[10][i][j];
            }
        }

        // Normalize images to the range [0, 1]
        cv::normalize(image1, image1, 0, 1, cv::NORM_MINMAX);
        cv::normalize(image2, image2, 0, 1, cv::NORM_MINMAX);

        // Create windows for visualization
        cv::namedWindow("Pitches 1", cv::WINDOW_NORMAL);
        cv::namedWindow("Timbre 1", cv::WINDOW_NORMAL);
        cv::namedWindow("Pitches 2", cv::WINDOW_NORMAL);
        cv::namedWindow("Timbre 2", cv::WINDOW_NORMAL);

        // Display images
        cv::imshow("Pitches 1", image1);
        cv::imshow("Timbre 1", image2);
        cv::imshow("Pitches 2", image1);
        cv::imshow("Timbre 2", image2);

        // Wait for user input to close windows
        cv::waitKey(0);

        // Destroy windows
        cv::destroyAllWindows();
    }

} // namespace Debug
