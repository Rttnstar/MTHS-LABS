#include <iostream>
#include <string>

using namespace std;

int main() {
    string s;
    getline(cin, s);

    for (size_t i = 0; i + 1 < s.length(); i++) {
        if (s[i] == '*' && s[i + 1] == '*') {
            s[i] = '1';
            s[i + 1] = '2';
            i++;
        }
    }

    cout << s << endl;

    return 0;
}