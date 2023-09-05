#include "Search.hpp"
#include "FeatureSimilarity.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <ctime>
#include <cstdlib>
#include <queue>

std::vector<std::pair<std::string, int>> Search::fuzzyGetSongTitle(const std::string &songTitle, const std::string &path, int threshold)
{
    std::vector<std::pair<std::string, int>> ratio;
    std::ifstream input(path, std::ios::binary);
    if (input)
    {
        std::vector<std::string> data;
        std::string line;
        while (std::getline(input, line))
        {
            data.push_back(line);
        }
        input.close();

        for (const std::string &item : data)
        {
            int score = fuzz::partial_ratio(songTitle, item);
            if (score >= threshold)
            {
                ratio.push_back(std::make_pair(item, score));
            }
        }
    }
    return ratio;
}

std::vector<std::pair<std::string, float>> Search::findSimilarSongs(const std::vector<float> &song, const std::vector<std::string> &paths, int numOfSongs, const std::vector<std::string> &excludeSongs, std::queue<std::vector<std::pair<std::string, float>>> &q)
{
    int batch = 5;
    if (paths.size() > batch)
    {
        std::vector<std::vector<std::string>> pathLists;
        int numBatches = paths.size() / batch;
        if (paths.size() % batch != 0)
        {
            numBatches++;
        }
        for (int i = 0; i < numBatches; i++)
        {
            int start = i * batch;
            int end = std::min((i + 1) * batch, static_cast<int>(paths.size()));
            std::vector<std::string> batchPaths(paths.begin() + start, paths.begin() + end);
            pathLists.push_back(batchPaths);
        }

        for (const std::vector<std::string> &pathList : pathLists)
        {
            std::unordered_map<std::string, std::vector<float>> data;
            for (const std::string &p : pathList)
            {
                std::ifstream input(p, std::ios::binary);
                if (input)
                {
                    std::unordered_map<std::string, std::vector<float>> songData;
                    input >> songData;
                    input.close();

                    for (const std::pair<std::string, std::vector<float>> &kv : songData)
                    {
                        const std::string &key = kv.first;
                        if (std::find(excludeSongs.begin(), excludeSongs.end(), key) == excludeSongs.end())
                        {
                            data[key] = kv.second;
                        }
                    }
                }
            }

            if (numOfSongs > static_cast<int>(data.size()))
            {
                numOfSongs = static_cast<int>(data.size()) - 1;
            }

            std::vector<std::pair<std::string, float>> similarSongs;
            for (const std::pair<std::string, std::vector<float>> &songData : data)
            {
                const std::string &songKey = songData.first;
                float cosSim = cosineSimilarity(song, songData.second);
                if (similarSongs.size() < static_cast<size_t>(numOfSongs))
                {
                    similarSongs.push_back(std::make_pair(songKey, cosSim));
                }
                else
                {
                    auto minSimSong = std::min_element(similarSongs.begin(), similarSongs.end(), [](const std::pair<std::string, float> &a, const std::pair<std::string, float> &b)
                                                       { return a.second < b.second; });
                    if (minSimSong->second < 0.8 && similarSongs.size() < static_cast<size_t>(numOfSongs))
                    {
                        break;
                    }
                    if (cosSim > minSimSong->second)
                    {
                        minSimSong->first = songKey;
                        minSimSong->second = cosSim;
                    }
                }
            }

            q.push(similarSongs);
        }
    }
    else
    {
        std::unordered_map<std::string, std::vector<float>> data;
        for (const std::string &p : paths)
        {
            std::ifstream input(p, std::ios::binary);
            if (input)
            {
                std::unordered_map<std::string, std::vector<float>> songData;
                input >> songData;
                input.close();

                for (const std::pair<std::string, std::vector<float>> &kv : songData)
                {
                    const std::string &key = kv.first;
                    if (std::find(excludeSongs.begin(), excludeSongs.end(), key) == excludeSongs.end())
                    {
                        data[key] = kv.second;
                    }
                }
            }
        }

        if (numOfSongs > static_cast<int>(data.size()))
        {
            numOfSongs = static_cast<int>(data.size()) - 1;
        }

        std::vector<std::pair<std::string, float>> similarSongs;
        for (const std::pair<std::string, std::vector<float>> &songData : data)
        {
            const std::string &songKey = songData.first;
            float cosSim = cosineSimilarity(song, songData.second);
            if (similarSongs.size() < static_cast<size_t>(numOfSongs))
            {
                similarSongs.push_back(std::make_pair(songKey, cosSim));
            }
            else
            {
                auto minSimSong = std::min_element(similarSongs.begin(), similarSongs.end(), [](const std::pair<std::string, float> &a, const std::pair<std::string, float> &b)
                                                   { return a.second < b.second; });
                if (minSimSong->second < 0.8 && similarSongs.size() < static_cast<size_t>(numOfSongs))
                {
                    break;
                }
                if (cosSim > minSimSong->second)
                {
                    minSimSong->first = songKey;
                    minSimSong->second = cosSim;
                }
            }
        }

        q.push(similarSongs);
    }

    std::vector<std::pair<std::string, float>> empty;
    return empty;
}

float Search::cosineSimilarity(const std::vector<float> &song1, const std::vector<float> &song2)
{
    if (song1[7] != song2[7])
    {
        return 0;
    }

    std::vector<float> weights = {0.05, 1, 1, 0.65, 0.5, 0.85, 0.4, 0.65, 0.15, 0.15, 0.15};
    std::vector<float> similarities(weights.size(), 0.0f);

    int j = 0;
    for (int i = 2; i <= 14; i++)
    {
        float similarity = 0.0f;
        if (i == 3)
        {
            similarity = FeatureSimilarity::methodDictionary[i](song1[i], song2[i], song1[i + 1], song2[i + 1]);
            if (similarity < 0.68)
            {
                return 0;
            }
        }
        else if (i == 5)
        {
            similarity = FeatureSimilarity::methodDictionary[i](song1[i], song2[i], song1[i + 2], song2[i + 2]);
            if (similarity < 0.5)
            {
                return 0;
            }
        }
        else
        {
            similarity = FeatureSimilarity::methodDictionary[i](song1[i], song2[i]);
        }

        if (similarity >= 0.05)
        {
            if (i == 9 && std::accumulate(similarities.begin(), similarities.end(), 0.0f) < 3)
            {
                return 0;
            }
            similarities[j] = similarity;
        }
        else
        {
            weights[j] = 0;
        }

        j++;
    }

    float dotProduct = std::inner_product(weights.begin(), weights.end(), similarities.begin(), 0.0f);
    float sumWeights = std::accumulate(weights.begin(), weights.end(), 0.0f);

    return dotProduct / sumWeights;
}

std::vector<std::pair<std::string, float>> Search::multiProcessing(const std::function<void(const std::vector<float> &, const std::vector<std::string> &, int, const std::vector<std::string> &, std::queue<std::vector<std::pair<std::string, float>>> &)> &func, int batch, const std::vector<float> &song, const std::vector<std::string> &excludeSongs, const std::vector<std::string> &pathList, int n)
{
    std::vector<std::string> shuffledPathList = pathList;
    std::random_shuffle(shuffledPathList.begin(), shuffledPathList.end());
    shuffledPathList.resize(6); // Limit to 6 paths (adjust as needed)

    std::vector<std::pair<std::string, float>> songList;
    int i = 0;
    std::queue<std::vector<std::pair<std::string, float>>> resultQueue;

    while (i < shuffledPathList.size())
    {
        int j = 0;
        while (j < batch)
        {
            if (i == shuffledPathList.size())
            {
                break;
            }

            std::vector<std::thread> threads;
            std::thread t(func, std::ref(song), std::ref(shuffledPathList[i]), n, std::ref(excludeSongs), std::ref(resultQueue));
            threads.push_back(std::move(t));
            i++;
            j++;
        }

        while (true)
        {
            try
            {
                std::vector<std::pair<std::string, float>> result = resultQueue.front();
                resultQueue.pop();
                songList.insert(songList.end(), result.begin(), result.end());
            }
            catch (std::exception &)
            {
                // Queue is empty, continue waiting
            }

            bool allExited = true;
            for (const std::thread &t : threads)
            {
                if (t.joinable())
                {
                    allExited = false;
                    break;
                }
            }

            if (allExited && resultQueue.empty())
            {
                break;
            }
        }
    }

    return songList;
}

std::vector<std::pair<std::string, float>> Search::reduceSongs(const std::vector<std::pair<std::string, float>> &songList, const std::vector<std::string> &pathList, int numOfSongs)
{
    std::vector<std::string> excludeSongs;
    for (const std::pair<std::string, float> &song : songList)
    {
        excludeSongs.push_back(song.first + '\0' + std::to_string(song.second));
    }

    std::vector<std::vector<float>> kmeansList;
    for (const std::pair<std::string, float> &song : songList)
    {
        kmeansList.push_back({0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f});
        kmeansList.back().insert(kmeansList.back().end(), song.second.begin() + 2, song.second.end());
    }

    std::vector<float> weights = {0.001f, 0.5f, 1.0f, 0.002f, 0.1f, 0.05f, 0.0002f};

    for (std::vector<float> &item : kmeansList)
    {
        for (size_t i = 0; i < item.size(); i++)
        {
            item[i] *= weights[i];
        }
    }

    int numClusters = std::min(static_cast<int>(songList.size() / 5) + 1, 4);
    KMeans kmeans(numClusters, 10000, 20);
    kmeans.fit(kmeansList);
    std::vector<std::vector<float>> centroids = kmeans.getCentroids();

    for (std::vector<float> &centroid : centroids)
    {
        for (size_t i = 0; i < centroid.size(); i++)
        {
            centroid[i] /= weights[i];
        }
    }

    std::vector<std::pair<std::string, float>> reducedSongList;
    for (size_t i = 0; i < songList.size() / 7 + 1; i++)
    {
        reducedSongList.push_back({"", ""});
        reducedSongList.back().insert(reducedSongList.back().end(), centroids[i].begin(), centroids[i].end());

        for (size_t l = 0; l < reducedSongList[i].size(); l++)
        {
            if (l == 3 || l == 4 || l == 7 || l == 8)
            {
                reducedSongList[i][l] = static_cast<int>(reducedSongList[i][l] + 0.5);
            }
        }

        std::vector<std::vector<float>> k;
        for (size_t j = 0; j < kmeans.getLabels().size(); j++)
        {
            if (kmeans.getLabels()[j] == static_cast<int>(i))
            {
                k.push_back(songList[j].second.begin() + 2, songList[j].second.end());
            }
        }

        reducedSongList[i] += averageArray(k);
    }

    std::vector<std::pair<std::string, float>> similarSongs;
    for (const std::pair<std::string, float> &song : reducedSongList)
    {
        std::vector<std::pair<std::string, float>> result = multiProcessing(findSimilarSongs, 8, song.second, excludeSongs, pathList, numOfSongs);
        similarSongs.insert(similarSongs.end(), result.begin(), result.end());
    }

    std::sort(similarSongs.begin(), similarSongs.end(), takeSecond);
    similarSongs.erase(std::unique(similarSongs.begin(), similarSongs.end()), similarSongs.end());

    return similarSongs;
}

std::vector<float> Search::averageArray(const std::vector<std::vector<float>> &arrays)
{
    std::vector<float> arr(arrays.size(), 0.0f);
    std::vector<float> a;
    for (size_t i = 0; i < arrays[0].size(); i++)
    {
        int minSize = 65;
        for (const std::vector<float> &array : arrays)
        {
            if (minSize > array[i].size())
            {
                minSize = array[i].size();
            }
        }
        for (const std::vector<float> &array : arrays)
        {
            std::vector<float> resizedArray;
            if (array[i].size() == 2)
            {
                cv::resize(array[i], resizedArray, cv::Size(12, minSize), 0, 0, cv::INTER_NEAREST);
            }
            else
            {
                resizedArray = cv::resize(array[i], cv::Size(1, minSize), 0, 0, cv::INTER_NEAREST);
            }
            a.push_back(static_cast<float>(cv::mean(resizedArray)[0]));
        }
        arr[i] = std::accumulate(a.begin(), a.end(), 0.0f) / a.size();
    }
    return arr;
}

bool Search::takeSecond(const std::pair<std::string, float> &elem)
{
    return elem.second > 0.0f;
}
