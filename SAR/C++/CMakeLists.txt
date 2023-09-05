cmake_minimum_required(VERSION 3.12)
project(Tunescape)

# Set C++ standard to C++11
set(CMAKE_CXX_STANDARD 11)

find_package(OpenSSL REQUIRED)
find_package(CURL REQUIRED)
find_package(spotify REQUIRED)  # Spotify library
find_package(OpenCV REQUIRED)   # Add this line for OpenCV

# Include directories for the libraries
include_directories(${OPENSSL_INCLUDE_DIR})
include_directories(${CURL_INCLUDE_DIRS})
include_directories(${SPOTIFY_INCLUDE_DIRS})  # Spotify library
include_directories(${OpenCV_INCLUDE_DIRS})     # Include OpenCV directories

add_executable(Tunescape
    src/Builder.cpp
    src/debug.cpp
    src/FeatureSimilarity.cpp
    src/run.cpp
    src/Search.cpp
    src/Spotify_Search_v4.cpp
)

# Link libraries
target_link_libraries(Tunescape
    ${OPENSSL_LIBRARIES}
    ${CURL_LIBRARIES}
    ${SPOTIFY_LIBRARIES}  # Spotify library
    ${OpenCV_LIBS}       # Link with OpenCV
)
