#ifndef SEARCH_HPP
#define SEARCH_HPP

#include <vector>
#include <string>
#include <queue>
#include <functional>
#include <unordered_map>

class Search
{
public:
    static std::vector<std::pair<std::string, int>> fuzzyGetSongTitle(const std::string &songTitle, const std::string &path, int threshold = 60);
    static std::vector<std::pair<std::string, float>> findSimilarSongs(const std::vector<float> &song, const std::vector<std::string> &paths, int numOfSongs = 1, const std::vector<std::string> &excludeSongs = {}, std::queue<std::vector<std::pair<std::string, float>>> &q = {});
    static float cosineSimilarity(const std::vector<float> &song1, const std::vector<float> &song2);
    static std::vector<std::pair<std::string, float>> multiProcessing(const std::function<void(const std::vector<float> &, const std::vector<std::string> &, int, const std::vector<std::string> &, std::queue<std::vector<std::pair<std::string, float>>> &)> &func, int batch, const std::vector<float> &song, const std::vector<std::string> &excludeSongs, const std::vector<std::string> &pathList, int n);
    static std::vector<std::pair<std::string, float>> reduceSongs(const std::vector<std::pair<std::string, float>> &songList, const std::vector<std::string> &pathList, int numOfSongs);

private:
    static std::vector<float> averageArray(const std::vector<std::vector<float>> &arrays);
    static bool takeSecond(const std::pair<std::string, float> &elem);
};

#endif // SEARCH_HPP
