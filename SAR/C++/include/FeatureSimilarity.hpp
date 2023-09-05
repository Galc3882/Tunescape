#ifndef FEATURE_SIMILARITY_HPP
#define FEATURE_SIMILARITY_HPP

#include <vector>
#include <string>
#include <functional>
#include <unordered_map>

class FeatureSimilarity
{
public:
    static std::vector<std::vector<float>> same_mode;
    static std::vector<std::vector<float>> min_maj;
    static std::vector<std::vector<float>> maj_min;

    static std::pair<std::vector<float>, std::vector<float>> equalizeDim(const std::vector<float> &l1, const std::vector<float> &l2);

    static float nb_cosine(const std::vector<float> &x, const std::vector<float> &y);

    static float key(int key1, int key2, int mode1, int mode2);

    static float speed(float tempo1, float tempo2, int time_signature1, int time_signature2);

    static float loudness(float loudness1, float loudness2);

    static float time_signature(int time_signature1, int time_signature2);

    static float year(int year1, int year2);

    static float duration(float duration1, float duration2);

    static float mode(int mode1, int mode2);

    static float sections_start(const std::vector<float> &sections_start1, const std::vector<float> &sections_start2);

    static float segments_pitches(const std::vector<std::vector<float>> &segments_pitches1, const std::vector<std::vector<float>> &segments_pitches2);

    static float segments_timbre(const std::vector<std::vector<float>> &segments_timbre1, const std::vector<std::vector<float>> &segments_timbre2);

    static float bars_start(const std::vector<float> &bars_start1, const std::vector<float> &bars_start2);

    static float tatums_start(const std::vector<float> &tatums_start1, const std::vector<float> &tatums_start2);

    static float beats_start(const std::vector<float> &beats_start1, const std::vector<float> &beats_start2);

    static float artist_name(const std::string &artist_name1, const std::string &artist_name2);

    static std::unordered_map<int, std::function<float(...)>> methodDictionary;
};

#endif // FEATURE_SIMILARITY_HPP
