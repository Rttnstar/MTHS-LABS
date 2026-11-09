#include <iostream>

using namespace std;

int main() {
    double a[20];
    for (int i = 0; i < 20; i++) {
        cin >> a[i];
    }

    for (int i = 9; i >= 0; i--) {
        cout << a[i + 10] << " " << a[i] << " ";
    }
    cout << endl;

    return 0;
}