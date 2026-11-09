#include <iostream>
#include <cstring>

using namespace std;

int main() {
    char string1[20] = "Hello";
    char string2[20] = "World";
    char string3[20];

    strcpy(string3, string1);
    cout << string3 << endl;

    strcat(string1, string2);
    cout << string1 << endl;

    cout << strlen(string1) << endl;

    char target[] = "Hello";
    if (strcmp(string3, target) == 0) {
        cout << "Equal" << endl;
    } else {
        cout << "Not Equal" << endl;
    }

    return 0;
}