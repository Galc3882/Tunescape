#include "Builder.hpp"
#include "hdf5_getters.hpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <tuple>
#include <opencv2/opencv.hpp>
#include <filesystem>
#include <ctime>
#include <chrono>
#include <cmath>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>

std::tuple<std::string, std::string, double, int, int, double, double, int, int, int, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<int>, std::vector<int>, std::vector<int>, std::vector<int>> Builder::getFeatures(const std::string &hdf5_file)
{
    std::vector<std::string> cropped_getters = {"get_title", "get_artist_name", "get_duration", "get_key",
                                                "get_mode", "get_tempo", "get_loudness", "get_time_signature",
                                                "get_year", "get_sections_start", "get_segments_pitches",
                                                "get_segments_timbre", "get_bars_start", "get_beats_start",
                                                "get_tatums_start"};

    H5File h5;
    h5.openH5FileRead(hdf5_file);

    std::tuple<std::string, std::string, double, int, int, double, double, int, int, int, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<int>, std::vector<int>, std::vector<int>, std::vector<int>> result;

    for (const std::string &getter : cropped_getters)
    {
        if (getter == "get_segments_pitches" || getter == "get_segments_timbre")
        {
            std::vector<std::vector<float>> res = hdf5_getters::__getattribute__(h5, getter, 0);
            if (res.size() > 64)
            {
                cv::Mat resized;
                cv::resize(cv::Mat(res), resized, cv::Size(12, 64), cv::INTER_CUBIC);
                res.resize(resized.rows);
                for (size_t i = 0; i < resized.rows; ++i)
                {
                    res[i].resize(resized.cols);
                    for (int j = 0; j < resized.cols; ++j)
                    {
                        res[i][j] = resized.at<float>(i, j);
                    }
                }
            }
            std::get<10>(result) = res;
        }
        else if (getter == "get_sections_start" || getter == "get_bars_start" || getter == "get_beats_start" || getter == "get_tatums_start")
        {
            std::vector<int> res = hdf5_getters::__getattribute__(h5, getter, 0);
            if (res.size() > 64)
            {
                std::vector<int> resized;
                cv::resize(cv::Mat(res), resized, cv::Size(1, 64), cv::INTER_NEAREST);
                std::get<12>(result) = resized;
            }
        }
        else
        {
            if (getter == "get_title" || getter == "get_artist_name")
            {
                std::string res = hdf5_getters::__getattribute__(h5, getter, 0);
                if (res.empty())
                {
                    res = "Unknown";
                }
                if (getter == "get_title")
                {
                    std::get<0>(result) = res;
                }
                else
                {
                    std::get<1>(result) = res;
                }
            }
            else if (getter == "get_duration" || getter == "get_key" || getter == "get_mode" || getter == "get_tempo" || getter == "get_loudness" || getter == "get_time_signature" || getter == "get_year")
            {
                double res = hdf5_getters::__getattribute__(h5, getter, 0);
                if (getter == "get_duration")
                {
                    std::get<2>(result) = res;
                }
                else if (getter == "get_key")
                {
                    std::get<3>(result) = static_cast<int>(res);
                }
                else if (getter == "get_mode")
                {
                    std::get<4>(result) = static_cast<int>(res);
                }
                else if (getter == "get_tempo")
                {
                    std::get<5>(result) = res;
                }
                else if (getter == "get_loudness")
                {
                    std::get<6>(result) = res;
                }
                else if (getter == "get_time_signature")
                {
                    std::get<7>(result) = static_cast<int>(res);
                }
                else if (getter == "get_year")
                {
                    std::get<8>(result) = static_cast<int>(res);
                }
            }
            else if (getter == "get_sections_start")
            {
                std::vector<int> res = hdf5_getters::__getattribute__(h5, getter, 0);
                if (res.size() > 64)
                {
                    std::vector<int> resized;
                    cv::resize(cv::Mat(res), resized, cv::Size(1, 64), cv::INTER_NEAREST);
                    std::get<12>(result) = resized;
                }
            }
        }
    }

    h5.close();

    return result;
}

void Builder::processChunk(const std::string &root, int chunkSize)
{
    std::string databasePath = "C:\\Users\\dkdkm\\Documents\\GitHub\\database\\";
    std::vector<std::string> lr = {"Black Market Hell\0Aiden",
                                   "Genuine\0Five Fingers of Funk", "bereit\0Panzer AG"};

    std::map<std::string, std::tuple<std::string, std::string, double, int, int, double, double, int, int, int, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<int>, std::vector<int>, std::vector<int>, std::vector<int>>> database;
    std::vector<std::string> pathList;

    for (const auto &entry : std::filesystem::recursive_directory_iterator(root))
    {
        if (entry.is_regular_file() && !entry.path().string().ends_with(".DS_Store"))
        {
            pathList.push_back(entry.path().string());
        }
    }

    std::vector<std::vector<std::string>> chunks;

    for (size_t i = 0; i < pathList.size(); i += chunkSize)
    {
        size_t end = std::min(i + chunkSize, pathList.size());
        std::vector<std::string> chunk(pathList.begin() + i, pathList.begin() + end);
        chunks.push_back(chunk);
    }

    for (size_t i = 0; i < chunks.size(); ++i)
    {
        std::cout << "Processing chunk " << i + 1 << " of " << chunks.size() << std::endl;
        auto startTime = std::chrono::high_resolution_clock::now();
        std::vector<std::future<std::tuple<std::string, std::string, double, int, int, double, double, int, int, int, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<std::vector<float>>, std::vector<int>, std::vector<int>, std::vector<int>, std::vector<int>>>> results;

        for (const std::string &file : chunks[i])
        {
            results.emplace_back(std::async(std::launch::async, Builder::getFeatures, file));
        }

        int lastIndex = 0;
        while (results.size() < chunks[i].size())
        {
            for (size_t j = 0; j < results.size(); ++j)
            {
                if (results[j].wait_for(std::chrono::seconds(0)) == std::future_status::ready)
                {
                    // Add to the database
                    auto features = results[j].get();
                    std::string key = std::get<0>(features) + "\0" + std::get<1>(features);
                    database[key] = features;
                    if (lr.size() > 0)
                    {
                        auto it = std::find(lr.begin(), lr.end(), key);
                        if (it != lr.end())
                        {
                            lr.erase(it);
                        }
                    }
                    results.erase(results.begin() + j);
                    break;
                }
            }
        }

        // Remove songs with no features
        for (const std::string &key : lr)
        {
            auto it = database.find(key);
            if (it != database.end())
            {
                database.erase(it);
            }
        }

        // Save the database to a pickle file
        std::string pickleFile = databasePath + "database" + std::to_string(i) + ".pickle";
        std::ofstream pickleStream(pickleFile, std::ios::binary);
        if (pickleStream)
        {
            pickleStream.write(reinterpret_cast<const char *>(&database), sizeof(database));
            pickleStream.close();
        }

        auto endTime = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::seconds>(endTime - startTime);
        std::cout << "Processing time: " << duration.count() << " seconds" << std::endl
                  << std::endl;

        // Clear the database
        database.clear();
    }
}
