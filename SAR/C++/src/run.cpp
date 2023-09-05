#include "Search.hpp"
#include "debug.hpp"
#include "Spotify_Search_v4.hpp"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iterator>
#include <ctime>
#include <chrono>
#include <filesystem>

void Search::getKey(Spotify_Search_v4& sp) {
    std::string songTitle;
    std::cout << "Enter the song title: ";
    std::cin >> songTitle;

    std::vector<std::vector<std::string>> songKey = sp.search(songTitle);

    if (songKey.size() > 1) {
        std::cout << "Multiple songs found:" << std::endl;
        for (size_t j = 0; j < songKey.size(); ++j) {
            std::cout << j + 1 << ". " << songKey[j][0] << " by " << songKey[j][1] << std::endl;
        }

        int k;
        std::cout << "Please enter the number of the song you want to use: ";
        std::cin >> k;

        if (k >= 1 && k <= static_cast<int>(songKey.size())) {
            std::cout << "'" << songKey[k - 1][0] << "'+'\0'+'" << songKey[k - 1][1] << "'+'\0'+'" << songKey[k - 1][8] << "'";
        } else {
            std::cout << "Invalid selection." << std::endl;
        }
    } else if (!songKey.empty()) {
        std::cout << songKey[0][0] << "\0" << songKey[0][1] << "\0" << songKey[0][8] << std::endl;
    } else {
        std::cout << "Song not found in Spotify." << std::endl;
    }
}

void Search::search(Spotify_Search_v4& sp, const std::vector<std::string>& songKey, const std::string& databasePath) {
    auto startTime = std::chrono::high_resolution_clock::now();
    std::vector<std::string> pathList;

    for (const auto& entry : std::filesystem::recursive_directory_iterator(databasePath)) {
        if (entry.is_regular_file()) {
            pathList.push_back(entry.path().string());
        }
    }

    std::vector<std::vector<std::string>> songValues;

    for (const std::string& key : songKey) {
        std::vector<std::string> parts;
        std::istringstream ss(key);
        std::string part;
        while (std::getline(ss, part, '\0')) {
            parts.push_back(part);
        }

        if (parts.size() < 3) {
            continue;
        }

        std::vector<std::string> features = sp.get_features(parts[2]);
        songValues.push_back({parts[0], parts[1]});
        songValues.back().insert(songValues.back().end(), features.begin(), features.end());
    }

    if (songValues.empty()) {
        std::cout << "No songs found in the database" << std::endl;
        return;
    }

    auto endTime = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::seconds>(endTime - startTime);

    std::cout << "That took " << duration.count() << " seconds" << std::endl;

    int numOfSongs = 5;
    std::vector<std::vector<std::string>> similarSongs = Search::reduceSongs(songValues, pathList, numOfSongs);

    if (similarSongs.size() > 20) {
        similarSongs.resize(20);
    }

    std::cout << "Similar Songs: " << std::endl;
    for (size_t i = 0; i < similarSongs.size(); ++i) {
        std::vector<std::string> songParts;
        std::istringstream ss(similarSongs[i][0]);
        std::string part;
        while (std::getline(ss, part, '\0')) {
            songParts.push_back(part);
        }
        if (songParts.size() >= 2) {
            std::cout << "Found Song: " << songParts[0] << " by " << songParts[1] << std::endl;
        }
        std::cout << "Cosine Similarity: " << similarSongs[i][1] << std::endl;
    }

    endTime = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::seconds>(endTime - startTime);

    std::cout << "That took " << duration.count() << " seconds" << std::endl;
}

void Search::compareTwoSongs(Spotify_Search_v4& sp, const std::string& song1, const std::string& song2, const std::string& databasePath) {
    std::vector<std::vector<std::string>> values;

    for (const std::string& key : {song1, song2}) {
        if (!key.empty() && key.back() == '\0') {
            std::vector<std::string> parts;
            std::istringstream ss(key);
            std::string part;
            while (std::getline(ss, part, '\0')) {
                parts.push_back(part);
            }
            if (parts.size() >= 3) {
                values.push_back({parts[0], parts[1]});
                std::vector<std::string> features = sp.get_features(parts[2]);
                values.back().insert(values.back().end(), features.begin(), features.end());
            }
        } else {
            std::vector<std::string> pathList;

            for (const auto& entry : std::filesystem::recursive_directory_iterator(databasePath)) {
                if (entry.is_regular_file()) {
                    pathList.push_back(entry.path().string());
                }
            }

            for (const std::string& path : pathList) {
                std::ifstream file(path);
                std::string line;
                while (std::getline(file, line)) {
                    std::istringstream iss(line);
                    std::vector<std::string> tokens;
                    std::string token;
                    while (std::getline(iss, token, '\t')) {
                        tokens.push_back(token);
                    }
                    if (tokens.size() >= 12 && tokens[0] == key) {
                        values.push_back({tokens[0], tokens[1]});
                        for (size_t i = 2; i < 12; ++i) {
                            values.back().push_back(tokens[i]);
                        }
                        break;
                    }
                }
                file.close();
            }
        }
    }

    if (values.size() == 2) {
        debug::compareSongs(values[0], values[1]);
    }
}

int main() {
    Spotify_Search_v4 sp = Spotify_Search_v4::authenticated_spotipy();

    Search::getKey(sp);

    // Example song key and database path
    std::vector<std::string> songKey = {"Money Trees\0Kendrick Lamar Jay Rock\02HbKqm4o0w5wEeEFXm2sD4"};
    std::string databasePath = r"C:\Users\dkdkm\Documents\GitHub\database";

    Search::search(sp, songKey, databasePath);

    // Example song keys for comparison (True for Spotify, False for MSD)
    std::string song1 = "Darts Of Pleasure\0Franz Ferdinand\07h0jDykw4RpWFqUhZQuElW";
    std::string song2 = "Love On A Mountain Top\x00Sinitta";

    Search::compareTwoSongs(sp, song1, song2, databasePath);

    return 0;
}