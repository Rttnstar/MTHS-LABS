#include <iostream>
#include <vector>

using namespace std;

void replaceMax(vector<int>& arr, int newValue) {
    if (arr.empty()) return;
    
    int maxIdx = 0;
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i] > arr[maxIdx]) {
            maxIdx = i;
        }
    }
    arr[maxIdx] = newValue;
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    int m;
    cin >> m;
    vector<int> b(m);
    for (int i = 0; i < m; i++) {
        cin >> b[i];
    }

    int k;
    cin >> k;

    replaceMax(a, k);
    replaceMax(b, 10);

    for (int i = 0; i < n; i++) {
        cout << a[i] << " ";
    }
    cout << endl;

    for (int i = 0; i < m; i++) {
        cout << b[i] << " ";
    }
    cout << endl;

    return 0;
}