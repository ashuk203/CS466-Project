#ifndef NW_H_
#define NW_H_

#include <string>
#include <iostream>

using namespace std;

int score(char a, char b);
void H();
int NW(string s1, string s2);
void init(int** DP, char ** bt, int len1, int len2, int gap);
int align(int** DP, char** bt, string s1, string s2, int gap);
int max(int v1, int v2, int v3, char * backptr);
#endif
