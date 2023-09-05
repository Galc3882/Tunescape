#ifndef SEARCH_HPP
#define SEARCH_HPP

#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <chrono>
#include "Spotify_Search_v4.hpp"

class Search
{
public:
    static void getKey(Spotify_Search_v4 &sp);
    static void search(Spotify_Search_v4 &sp, const std::vector<std::string> &songKey, const std::string &databasePath);
    static void compareTwoSongs(Spotify_Search_v4 &sp, const std::string &song1, const std::string &song2, const std::string &databasePath);
};

#endif // SEARCH_HPP
