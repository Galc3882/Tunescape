# Tunescape: A Symphony of Music Recommendation Innovation

## Introduction

Welcome to the world of Tunescape, where the boundaries of music discovery are shattered and replaced with a dynamic, personalized, and highly immersive experience. Tunescape is not just another music recommendation service; it's a groundbreaking project that marries the realms of music theory, data science, and software engineering to create a truly unique listening journey. This README is your gateway to understanding the profound purpose, intricate workings, and the compelling fusion of C++ and Python that power Tunescape.

## Purpose

Tunescape's raison d'être is clear: to provide users with recommendations that transcend the confines of traditional genre-based systems. Instead, it delves deep into the rich tapestry of a song's intrinsic characteristics, such as key signature, tempo, and more, to offer recommendations that resonate profoundly with users. Tunescape recognizes that individuals with musical training or discerning ears often connect on a deeper level with these subtle features. Thus, Tunescape's recommendations are curated to cater to the musical connoisseur in you.

## Overview

Tunescape is a sophisticated algorithmic platform that elevates music recommendation to an art form. Let's embark on a detailed journey to uncover its inner workings:

### Spotify Integration

Tunescape integrates seamlessly with the Spotify API, leveraging it for track information and in-depth audio analysis. This integration is at the core of Tunescape's ability to provide rich and relevant recommendations.

### Feature Extraction

The personalized experience begins with the extraction of essential musical features from selected tracks:

- **Duration**: The length of the song.
- **Key**: The key signature of the song.
- **Mode**: Whether the song is in major or minor mode.
- **Tempo**: The tempo or beats per minute (BPM).
- **Loudness**: A measure of the song's volume.
- **Time Signature**: The time signature, indicating the number of beats in a bar.
- **Year**: The release year of the song.
- **Section Starts**: Timestamps marking the start of song sections.
- **Segment Pitches**: Pitch information for song segments.
- **Segment Timbre**: Timbral characteristics for song segments.
- **Bars Start**: Timestamps marking the start of bars in the song.
- **Beats Start**: Timestamps marking the start of beats in the song.
- **Tatums Start**: Timestamps marking the start of tatums in the song.

### Feature Comparison

Tunescape employs an array of advanced techniques to compare these extracted features. This includes methods like cosine similarity and more, ensuring that recommendations are not limited to broad genre categories but capture the intricate essence of each song.

### Database Processing

To achieve this feat, Tunescape relies on a substantial database of 1-million songs. Each song's features are meticulously stored, indexed, and prepared for efficient comparison. This extensive database is at the heart of Tunescape's ability to deliver precise recommendations.

### User-Centric Recommendations

Tunescape's recommendations are anything but generic. They are curated to align with individual user preferences. Users with musical training or a knack for identifying subtle musical traits are sure to appreciate the precision and depth of Tunescape's recommendations.

## Detailed Walkthrough of the Code and Features

Tunescape's codebase is a testament to precision engineering, blending C++ and Python to create a harmonious symphony of software components.

### C++/Python Components

Let's delve into the technical aspects of the C++ and Python components that form the backbone of Tunescape:

#### `Builder.hpp/cpp - Builder.py`

- **Purpose**: The Builder module is responsible for constructing and populating the music database by extracting and processing features from HDF5 files containing song information.
- **Key Functions**:
  - The Builder module handles the complexity of data extraction, cleansing, and storage, making it an integral part of Tunescape's data processing pipeline.
  - The use of multiprocessing significantly enhances the performance of feature extraction, allowing Tunescape to process a large number of songs efficiently.
  - Features like pitch, timbre, and time signatures are transformed and resized to ensure consistent data format for compatibility with the recommendation engine.
  - The resulting database is cleaned by removing songs with missing features or specific known issues.

#### `debug.hpp/cpp - debug.py`

- **Purpose**: Debugging utilities that ensure the algorithm operates flawlessly during development and testing.
- **Key Functions**:
  - Profiling tools are instrumental in identifying performance bottlenecks and optimizing code execution.
  - Feature comparison techniques help in assessing the effectiveness of the recommendation system.
  - Visualizations enhance debugging and provide a visual representation of feature comparisons.
  - The module's flexibility allows developers to fine-tune the system and make performance improvements.

#### `FeatureSimilarity.hpp/cpp - FeatureSimilarity.py`

- **Purpose**: Implements various methods for comparing song features, guaranteeing the precision of recommendations.
- **Key Functions**:
  - The module uses mathematical and statistical techniques to quantify the similarity between musical features. For instance, cosine similarity measures the cosine of the angle between two feature vectors, providing a similarity score between 0 and 1.
  - To handle feature vectors with varying dimensions, the `equalizeDim` function pads shorter lists with zeros.
  - Numba is employed to optimize the performance of the `nb_cosine` function, making it well-suited for processing large datasets efficiently.
  - The `methodDictionary` facilitates dynamic selection of similarity functions based on the specific features being compared.

#### `run.hpp/cpp - run.py`

- **Purpose**: Houses the core logic for running Tunescape's recommendation engine, orchestrating the entire process.
- **Key Functions**: Contains the main execution flow for generating recommendations.

#### `Search.hpp/cpp - Search.py`

- **Purpose**: Facilitates functionality for searching and reducing songs based on their features, particularly using cosine similarity and K-means clustering. It supports searching for similar songs and reducing the number of songs to provide recommendations.
- **Key Functions**:
  - The module uses fuzzy string matching to search for song titles in the database.
  - Cosine similarity is computed based on various musical features.
  - K-means clustering is employed to group similar songs and reduce their number.
  - The module supports parallel processing for performance optimization.

#### `Spotify_Search_v4.hpp/cpp - Spotify_Search_v4.py`

- **Purpose**: Handles Spotify authentication and interaction, including searching for tracks and extracting features.
- **Key Functions**: Manages the connection to Spotify, ensuring seamless integration with Tunescape.

#### `CMakeLists.txt`

- **Purpose**: The CMake configuration file responsible for building the C++ components.

### Requirements

Tunescape operates on a carefully curated set of requirements and adheres to a structured file architecture:

- **CMake 3.12 or Later**: Enables seamless building and configuration of C++ components.
- **libcurl**: Used for making HTTP requests, a fundamental part of Spotify API interaction.
- **libcurlpp**: A C++ wrapper for libcurl, enhancing the integration of libcurl into the C++ components.
- **libspotify**: The Spotify API library, enabling Tunescape's integration with Spotify.
- **Python 3.6 or Later**: A prerequisite for running the Python components.
- **Spotipy**: A Python library that facilitates interaction with the Spotify API.
- **Fuzzywuzzy**: A Python library used for fuzzy string matching, enhancing the accuracy of search and comparison operations.

### File Architecture

The project structure is organized for clarity and efficiency:

- **SAR**: The main project directory.
  - **SAR/C++**: Houses the C++ source code.
    - **SAR/C++/include**: Contains header files for C++ components.
    - **SAR/C++/src**: Stores C++ source files that constitute the core of Tunescape.
    - **SAR/C++/CMakeLists.txt**: The CMake configuration file that orchestrates the building of C++ components.
  - **SAR/python**: Home to the Python source code.
    - Various Python scripts that handle database processing, feature comparison, Spotify interaction, and more.

## Conclusion

Tunescape represents an exciting exploration of how art and science can harmoniously coexist to create a deeply personal and immersive music discovery experience. The fusion of C++ and Python showcases the versatility and expertise of the developers behind this groundbreaking project.

## Next Steps

- [ ] **Explore Additional Musical Features**: Continuously expand the set of musical features considered for even more precise recommendations.
- [ ] **Expand Music Database**: Broaden the horizons of the music database to include an even wider range of songs and genres, ensuring that Tunescape caters to every taste.
- [ ] **Collaborate with Streaming Platforms**: Forge partnerships with music streaming platforms to seamlessly integrate Tunescape's innovative recommendation algorithm.
- [ ] **User Feedback Mechanisms**: Implement feedback loops that empower users to contribute to the refinement of recommendations, ensuring a continually improving music discovery experience.


<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
