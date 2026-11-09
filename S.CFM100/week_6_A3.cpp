#include <iostream>

using namespace std;

long long factorial(int n) {
    long long fact = 1;
    for (int i = 1; i <= n; i++) {
        fact *= i;
    }
    return fact;
}

int main() {
    int N;
    cin >> N;

    long long tegsh_fact_sum = 0;
    long long sondgoi_fact_sum = 0;

    for (int i = 1; i <= N; i++) {
        if (i % 2 == 0) {
            tegsh_fact_sum += factorial(i);
        } else {
            sondgoi_fact_sum += factorial(i);
        }
    }

    cout << "Тэгш тоонуудын факториалын нийлбэр: " << tegsh_fact_sum << endl;
    cout << "Сондгой тоонуудын факториалын нийлбэр: " << sondgoi_fact_sum << endl;

    return 0;
}