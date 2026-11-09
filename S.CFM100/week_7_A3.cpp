#include <iostream>

using namespace std;

int main() {
    int A[3][3], B[3][3];

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cin >> A[i][j];
        }
    }

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cin >> B[i][j];
        }
    }

    bool equal = true;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (A[i][j] != B[i][j]) {
                equal = false;
                break;
            }
        }
        if (!equal) break;
    }

    if (equal) {
        cout << "Тэнцүү" << endl;
    } else {
        cout << "Тэнцүү биш" << endl;
    }

    return 0;
}