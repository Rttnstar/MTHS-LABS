#include <iostream>
#include <cmath>

using namespace std;

double p(double y, double a[]) {
    double sum = 0;
    for (int i = 0; i <= 6; i++) {
        sum += a[i] * pow(y, i);
    }
    return sum;
}

int main() {
    double a[7];
    for (int i = 0; i <= 6; i++) {
        cin >> a[i];
    }

    int x_values[] = {1, 3, 4};
    for (int i = 0; i < 3; i++) {
        int x = x_values[i];
       double diff = p(x + 1, a) - p(x, a);
        cout << "x = " << x << " үед: " << diff << endl;
    }

    return 0;
}
