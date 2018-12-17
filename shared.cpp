#include <iostream>
#include <limits>
using namespace std;

int score(char base1, char base2) {
  int ascii_1 = (int) base1;
  int ascii_2 = (int) base2;

  if (ascii_1 == 45 or ascii_2 == 45) {
    if (ascii_1 == 45 and ascii_2 == 45) {
      return numeric_limits<int>::min();
    }
  }

  if (ascii_1 == ascii_2) {
    return 1;
  }

  return -1;
}
