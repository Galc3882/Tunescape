#ifndef SPOTIFYSEARCH_HPP
#define SPOTIFYSEARCH_HPP

#include <string>
#include <vector>

// Struct to store track information
struct TrackInfo {
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
struct TrackFeatures {
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

class SpotifySearch {
public:
    // Constructor for initializing Spotify authentication
    SpotifySearch(const std::string& clientId, const std::string& clientSecret);

    // Authenticate with Spotify and obtain an access token
    bool AuthenticateSpotify();

    // Search for tracks on Spotify
    std::vector<TrackInfo> SearchSpotifyTrack(const std::string& trackName);

    // Get track features from Spotify
    TrackFeatures GetSpotifyTrackFeatures(const std::string& trackId);

private:
    // Spotify API endpoints and client credentials
    const std::string BASE_URL = "https://accounts.spotify.com/api/token";
    const std::string CLIENT_ID;
    const std::string CLIENT_SECRET;

    // Access token obtained during authentication
    std::string ACCESS_TOKEN;

    // Callback function for writing HTTP response to a string
    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* output);
};

#endif // SPOTIFYSEARCH_HPP
