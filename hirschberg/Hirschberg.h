#ifndef HSCHB_H_
#define HSCHB_H_

#include <string>
#include <iostream>
#include <vector>
#include <utility>


using namespace std;


int* forwardHirsch(string, string);
int* backwardHirsch(string, string);
void hirschberg_helper(string, string, vector<pair<int, int> >, int, int);
void hirschberg(string, string);


#endif
