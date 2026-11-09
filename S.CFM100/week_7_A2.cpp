#include <iostream>

using namespace std;

int main() {
    double A[8];
    for (int i = 0; i < 8; i++) {
        cin >> A[i];
    }

    double X;
    cin >> X;

    int count = 0;
    for (int i = 0; i < 8; i++) {
        if (A[i] < X) {
            cout << "Индекс (дугаар): " << i << ", Утга: " << A[i] << endl;
            count++;
        }
    }

    cout << "Нөхцөл хангасан элементийн тоо: " << count << endl;

    return 0;
}