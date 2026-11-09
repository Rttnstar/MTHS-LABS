#include <iostream>

using namespace std;

struct Rectangle {
    double width;
    double height;

    double area() {
        return width * height;
    }
};

int main() {
    Rectangle rect;
    cin >> rect.width >> rect.height;

    cout << "Талбай: " << rect.area() << endl;

    return 0;
}