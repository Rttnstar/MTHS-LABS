#include <iostream>
using namespace std;
int main (){
  int m, n, r;
  cout << "m bolon n toonuudiig oruulna uu";
    cin >> m >> n;
  while (n !=0){
    r = m % n;
    m = n;
    n = r;

  }
  cout << "GCD =" << m << endl;
  return 0;
}
