#include "FeatureSimilarity.hpp"
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <numeric>

std::vector<std::vector<float>> FeatureSimilarity::same_mode = {
    {1, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 0, 0.8333, 0.6667, 0.5, 0.3333, 0.16667}};

std::vector<std::vector<float>> FeatureSimilarity::min_maj = {
    {0.4286, 0.5714, 0.1429, 0.8571, 0.1429, 0.5714, 0.4286, 0.2857, 0.7143, 0, 0.7143, 0.2857}};

std::vector<std::vector<float>> FeatureSimilarity::maj_min = {
    {0.4286, 0.2857, 0.7143, 0, 0.7143, 0.2857, 0.4286, 0.5714, 0.1429, 0.8571, 0.1429, 0.5714}};

std::pair<std::vector<float>, std::vector<float>> FeatureSimilarity::equalizeDim(const std::vector<float> &l1, const std::vector<float> &l2)
{
    std::vector<float> result1 = l1;
    std::vector<float> result2 = l2;

    if (result1.empty())
    {
        result1 = std::vector<float>(l2.size(), 0);
    }
    else if (result2.empty())
    {
        result2 = std::vector<float>(l1.size(), 0);
    }
    else
    {
        while (result1.size() < result2.size())
        {
            result1.push_back(0);
        }

        while (result2.size() < result1.size())
        {
            result2.push_back(0);
        }
    }

    return std::make_pair(result1, result2);
}

float FeatureSimilarity::nb_cosine(const std::vector<float> &x, const std::vector<float> &y)
{
    float max_x = *std::max_element(x.begin(), x.end());
    float min_x = *std::min_element(x.begin(), x.end());
    float max_y = *std::max_element(y.begin(), y.end());
    float min_y = *std::min_element(y.begin(), y.end());

    float m = std::max(max_x, max_y) - std::min(min_x, min_y);

    return std::max(1 - std::abs(std::inner_product(x.begin(), x.end(), y.begin(), 0.0) / (x.size() * m)), 0.0f);
}

float FeatureSimilarity::key(int key1, int key2, int mode1, int mode2)
{
    if (mode1 == mode2)
    {
        return same_mode[0][key2 - key1];
    }
    else if (mode1 == 0 && mode2 == 1)
    {
        return min_maj[0][key2 - key1];
    }
    else
    {
        return maj_min[0][key1 - key2];
    }
}

float FeatureSimilarity::speed(float tempo1, float tempo2, int time_signature1, int time_signature2)
{
    if (tempo1 == tempo2 && time_signature1 == time_signature2)
    {
        return 1;
    }
    return std::max(1 - 0.03f * std::abs(tempo1 / time_signature1 - tempo2 / time_signature2), 0.0f);
}

float FeatureSimilarity::loudness(float loudness1, float loudness2)
{
    return std::max(1 - 0.4f * std::abs(loudness1 - loudness2), 0.0f);
}

float FeatureSimilarity::time_signature(int time_signature1, int time_signature2)
{
    if (time_signature1 == time_signature2)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

float FeatureSimilarity::year(int year1, int year2)
{
    if (year1 < 1800 || year2 < 1800)
    {
        return -1;
    }
    return std::max(1 - 0.1f * std::abs(year1 - year2), 0.0f);
}

float FeatureSimilarity::duration(float duration1, float duration2)
{
    return std::max(1 - 0.005f * std::abs(duration1 - duration2), 0.0f);
}

float FeatureSimilarity::mode(int mode1, int mode2)
{
    return (mode1 == mode2) ? 1 : 0;
}

float FeatureSimilarity::sections_start(const std::vector<float> &sections_start1, const std::vector<float> &sections_start2)
{
    if (sections_start1.empty() || sections_start2.empty())
    {
        return 0;
    }

    std::vector<float> result1 = sections_start1;
    std::vector<float> result2 = sections_start2;

    if (result1.size() > result2.size())
    {
        result1.resize(result2.size());
    }
    else if (result2.size() > result1.size())
    {
        result2.resize(result1.size());
    }

    return nb_cosine(result1, result2);
}

float FeatureSimilarity::segments_pitches(const std::vector<std::vector<float>> &segments_pitches1, const std::vector<std::vector<float>> &segments_pitches2)
{
    if (segments_pitches1.size() > segments_pitches2.size())
    {
        std::vector<std::vector<float>> resized_pitches1(segments_pitches1.begin(), segments_pitches1.begin() + segments_pitches2.size());
        return nb_cosine(resized_pitches1, segments_pitches2);
    }
    else if (segments_pitches2.size() > segments_pitches1.size())
    {
        std::vector<std::vector<float>> resized_pitches2(segments_pitches2.begin(), segments_pitches2.begin() + segments_pitches1.size());
        return nb_cosine(segments_pitches1, resized_pitches2);
    }
    else
    {
        return nb_cosine(segments_pitches1, segments_pitches2);
    }
}

float FeatureSimilarity::segments_timbre(const std::vector<std::vector<float>> &segments_timbre1, const std::vector<std::vector<float>> &segments_timbre2)
{
    if (segments_timbre1.size() > segments_timbre2.size())
    {
        std::vector<std::vector<float>> resized_timbre1(segments_timbre1.begin(), segments_timbre1.begin() + segments_timbre2.size());
        return nb_cosine(resized_timbre1, segments_timbre2);
    }
    else if (segments_timbre2.size() > segments_timbre1.size())
    {
        std::vector<std::vector<float>> resized_timbre2(segments_timbre2.begin(), segments_timbre2.begin() + segments_timbre1.size());
        return nb_cosine(segments_timbre1, resized_timbre2);
    }
    else
    {
        return nb_cosine(segments_timbre1, segments_timbre2);
    }
}

float FeatureSimilarity::bars_start(const std::vector<float> &bars_start1, const std::vector<float> &bars_start2)
{
    if (bars_start1.empty() || bars_start2.empty())
    {
        return 0;
    }

    std::vector<float> result1 = bars_start1;
    std::vector<float> result2 = bars_start2;

    if (result1.size() > result2.size())
    {
        result1.resize(result2.size());
    }
    else if (result2.size() > result1.size())
    {
        result2.resize(result1.size());
    }

    return nb_cosine(result1, result2);
}

float FeatureSimilarity::tatums_start(const std::vector<float> &tatums_start1, const std::vector<float> &tatums_start2)
{
    if (tatums_start1.empty() || tatums_start2.empty())
    {
        return 0;
    }

    std::vector<float> result1 = tatums_start1;
    std::vector<float> result2 = tatums_start2;

    if (result1.size() > result2.size())
    {
        result1.resize(result2.size());
    }
    else if (result2.size() > result1.size())
    {
        result2.resize(result1.size());
    }

    return nb_cosine(result1, result2);
}

float FeatureSimilarity::beats_start(const std::vector<float> &beats_start1, const std::vector<float> &beats_start2)
{
    if (beats_start1.empty() || beats_start2.empty())
    {
        return 0;
    }

    std::vector<float> result1 = beats_start1;
    std::vector<float> result2 = beats_start2;

    if (result1.size() > result2.size())
    {
        result1.resize(result2.size());
    }
    else if (result2.size() > result1.size())
    {
        result2.resize(result1.size());
    }

    return nb_cosine(result1, result2);
}

float FeatureSimilarity::artist_name(const std::string &artist_name1, const std::string &artist_name2)
{
    return (artist_name1 == artist_name2) ? 1.0f : 0.0f;
}

std::unordered_map<int, std::function<float(...)>> FeatureSimilarity::methodDictionary = {
    {1, &FeatureSimilarity::artist_name},
    {2, &FeatureSimilarity::duration},
    {3, &FeatureSimilarity::key},
    {5, &FeatureSimilarity::speed},
    {6, &FeatureSimilarity::loudness},
    {8, &FeatureSimilarity::year},
    {9, &FeatureSimilarity::sections_start},
    {10, &FeatureSimilarity::segments_pitches},
    {11, &FeatureSimilarity::segments_timbre},
    {12, &FeatureSimilarity::bars_start},
    {13, &FeatureSimilarity::beats_start},
    {14, &FeatureSimilarity::tatums_start}};
