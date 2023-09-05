#ifndef DEBUG_HPP
#define DEBUG_HPP

#include <vector>
#include <string>

namespace Debug
{

    void main(const std::vector<float> &songValue, const std::vector<std::string> &pathList);
    void performanceTest();
    void printValues(const std::vector<float> &values);
    void compareValues(const std::vector<float> &values1, const std::vector<float> &values2);
    void compareSongs(const std::vector<float> &values1, const std::vector<float> &values2);

} // namespace Debug

#endif // DEBUG_HPP
