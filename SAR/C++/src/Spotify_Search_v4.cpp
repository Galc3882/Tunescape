#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <sstream>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <chrono>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

// Define the Spotify API endpoints and your client credentials
const std::string BASE_URL = "https://accounts.spotify.com/api/token";
const std::string CLIENT_ID = "d513b538756244beaabe189f5ba75be1";
const std::string CLIENT_SECRET = "943e6dab04c34d78a05752b515e3fb2a";

std::string ACCESS_TOKEN;

// Struct to store track information
struct TrackInfo
{
    std::string name;
    std::string artists;
    std::string duration;
    std::string album_art;
    std::string release_date;
    int popularity;
    bool isExplicit;
    std::string url;
    std::string id;
};

// Struct to store track features
struct TrackFeatures
{
    int duration;
    int key;
    int mode;
    double tempo;
    double loudness;
    int time_signature;
    int year;
    std::vector<double> section_starts;
    std::vector<std::vector<double>> segment_pitches;
    std::vector<std::vector<double>> segment_timbre;
    std::vector<double> bars_start;
    std::vector<double> beats_start;
    std::vector<double> tatums_start;
};

// Callback function for writing HTTP response to a string
size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *output)
{
    size_t total_size = size * nmemb;
    output->append(static_cast<char *>(contents), total_size);
    return total_size;
}

// Function to perform Spotify authentication and obtain an access token
bool AuthenticateSpotify()
{
    // Construct the base64-encoded client credentials
    std::string base64_creds = CLIENT_ID + ":" + CLIENT_SECRET;
    CURL *curl;
    CURLcode res;
    std::string readBuffer;

    // Initialize libcurl
    curl = curl_easy_init();
    if (curl)
    {
        // Set the authentication URL
        curl_easy_setopt(curl, CURLOPT_URL, "https://accounts.spotify.com/api/token");
        // Specify that we want to perform a POST request
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        // Set the request headers
        struct curl_slist *headers = nullptr;
        headers = curl_slist_append(headers, "Content-Type: application/x-www-form-urlencoded");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        // Construct the request body
        std::string postFields = "grant_type=client_credentials";
        // Set the request body
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postFields.c_str());
        // Set the write callback function
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        // Perform the HTTP request
        res = curl_easy_perform(curl);
        // Clean up libcurl
        curl_easy_cleanup(curl);
        if (res != CURLE_OK)
        {
            std::cerr << "Authentication request failed: " << curl_easy_strerror(res) << std::endl;
            return false;
        }
    }
    else
    {
        std::cerr << "Error initializing libcurl." << std::endl;
        return false;
    }

    // Parse the JSON response to obtain the access token
    nlohmann::json auth_data = nlohmann::json::parse(readBuffer);
    ACCESS_TOKEN = auth_data["access_token"];
    return true;
}

// Function to search for tracks on Spotify
std::vector<TrackInfo> SearchSpotifyTrack(const std::string &trackName)
{
    std::vector<TrackInfo> tracks;
    CURL *curl;
    CURLcode res;
    std::string readBuffer;

    // Initialize libcurl
    curl = curl_easy_init();
    if (curl)
    {
        // Construct the search query
        std::string query = BASE_URL + "/search?type=track&q=" + trackName;
        // Set the request URL
        curl_easy_setopt(curl, CURLOPT_URL, query.c_str());
        // Set the request headers (include the access token)
        struct curl_slist *headers = nullptr;
        std::string authHeader = "Authorization: Bearer " + ACCESS_TOKEN;
        headers = curl_slist_append(headers, authHeader.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        // Set the write callback function
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        // Perform the HTTP request
        res = curl_easy_perform(curl);
        // Clean up libcurl
        curl_easy_cleanup(curl);
        if (res != CURLE_OK)
        {
            std::cerr << "Track search request failed: " << curl_easy_strerror(res) << std::endl;
            return tracks;
        }
    }
    else
    {
        std::cerr << "Error initializing libcurl." << std::endl;
        return tracks;
    }

    // Parse the JSON response to extract track information
    nlohmann::json search_data = nlohmann::json::parse(readBuffer);
    nlohmann::json tracks_data = search_data["tracks"]["items"];
    for (const auto &track : tracks_data)
    {
        TrackInfo trackInfo;
        trackInfo.name = track["name"];
        trackInfo.artists = "";
        for (const auto &artist : track["artists"])
        {
            trackInfo.artists += artist["name"].get<std::string>() + " ";
        }
        trackInfo.artists = trackInfo.artists.substr(0, trackInfo.artists.size() - 1); // Remove trailing space
        trackInfo.duration = track["duration_ms"];
        trackInfo.album_art = track["album"]["images"][2]["url"];
        trackInfo.release_date = track["album"]["release_date"];
        trackInfo.popularity = track["popularity"];
        trackInfo.isExplicit = track["explicit"];
        trackInfo.url = track["external_urls"]["spotify"];
        trackInfo.id = track["id"];
        tracks.push_back(trackInfo);
    }
    return tracks;
}

// Function to get track features from Spotify
TrackFeatures GetSpotifyTrackFeatures(const std::string &trackId)
{
    TrackFeatures trackFeatures;
    CURL *curl;
    CURLcode res;
    std::string readBuffer;

    // Initialize libcurl
    curl = curl_easy_init();
    if (curl)
    {
        // Construct the track features URL
        std::string url = BASE_URL + "/audio-features/" + trackId;
        // Set the request URL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        // Set the request headers (include the access token)
        struct curl_slist *headers = nullptr;
        std::string authHeader = "Authorization: Bearer " + ACCESS_TOKEN;
        headers = curl_slist_append(headers, authHeader.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        // Set the write callback function
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        // Perform the HTTP request
        res = curl_easy_perform(curl);
        // Clean up libcurl
        curl_easy_cleanup(curl);
        if (res != CURLE_OK)
        {
            std::cerr << "Track features request failed: " << curl_easy_strerror(res) << std::endl;
            return trackFeatures;
        }
    }
    else
    {
        std::cerr << "Error initializing libcurl." << std::endl;
        return trackFeatures;
    }

    // Parse the JSON response to extract track features
    nlohmann::json features_data = nlohmann::json::parse(readBuffer);
    trackFeatures.duration = features_data["duration_ms"];
    trackFeatures.key = features_data["key"];
    trackFeatures.mode = features_data["mode"];
    trackFeatures.tempo = features_data["tempo"];
    trackFeatures.loudness = features_data["loudness"];
    trackFeatures.time_signature = features_data["time_signature"];
    trackFeatures.year = 0; // TODO: Add Year
    trackFeatures.section_starts = features_data["sections"].get<std::vector<double>>();
    trackFeatures.segment_pitches = features_data["segments"]["pitches"].get<std::vector<std::vector<double>>>();
    trackFeatures.segment_timbre = features_data["segments"]["timbre"].get<std::vector<std::vector<double>>>();
    trackFeatures.bars_start = features_data["bars"].get<std::vector<double>>();
    trackFeatures.beats_start = features_data["beats"].get<std::vector<double>>();
    trackFeatures.tatums_start = features_data["tatums"].get<std::vector<double>>();
    return trackFeatures;
}

int main()
{
    // Authenticate with Spotify
    if (!AuthenticateSpotify())
    {
        std::cerr << "Authentication failed." << std::endl;
        return 1;
    }

    // Search for tracks
    std::string trackName = "Sweet Caroline";
    std::vector<TrackInfo> tracks = SearchSpotifyTrack(trackName);
    if (tracks.empty())
    {
        std::cerr << "No tracks found for '" << trackName << "'" << std::endl;
        return 1;
    }

    // Get features for the first track in the search results
    TrackFeatures features = GetSpotifyTrackFeatures(tracks[0].id);

    // Print track information and features
    std::cout << "Track Information:" << std::endl;
    std::cout << "Name: " << tracks[0].name << std::endl;
    std::cout << "Artists: " << tracks[0].artists << std::endl;
    std::cout << "Duration: " << tracks[0].duration << " ms" << std::endl;
    std::cout << "Album Art: " << tracks[0].album_art << std::endl;
    std::cout << "Release Date: " << tracks[0].release_date << std::endl;
    std::cout << "Popularity: " << tracks[0].popularity << std::endl;
    std::cout << "Explicit: " << (tracks[0].isExplicit ? "Yes" : "No") << std::endl;
    std::cout << "Spotify URL: " << tracks[0].url << std::endl;
    std::cout << "ID: " << tracks[0].id << std::endl;

    std::cout << "\nTrack Features:" << std::endl;
    std::cout << "Duration: " << features.duration << " ms" << std::endl;
    std::cout << "Key: " << features.key << std::endl;
    std::cout << "Mode: " << features.mode << std::endl;
    std::cout << "Tempo: " << features.tempo << std::endl;
    std::cout << "Loudness: " << features.loudness << std::endl;
    std::cout << "Time Signature: " << features.time_signature << std::endl;
    std::cout << "Year: " << features.year << std::endl;
    std::cout << "Section Starts:" << std::endl;
    for (const auto &start : features.section_starts)
    {
        std::cout << start << " ";
    }
    std::cout << std::endl;

    return 0;
}
