#include <ctime> 
#include "NeedlemanWunsch.h"

using namespace std;

int main() {
	H();
	NW("ab", "cd");

	cout << "Compilation test 2" << endl; \
		return 0;
}

//implementaiton of Hirshberg Alg.
void H() {
	return;
}


//implementaiton of Needleman-Wunsch Alg.
int NW(string s1, string s2) {

	// memory and time tracking
	unsigned long memory_usage = 0;
	double duration;
	clock_t clock_start = clock();

	//gap penalty
	int gap = 1;

	//sequence lengths
	int len1 = s1.length();
	int len2 = s2.length();

	//create DP table
	int **DP = new int *[len2 + 1];
	memory_usage += (DP + (len2 + 1)) - DP;
	for (int i = 0; i <= len2; i++) {
		DP[i] = new int[len1];
		memory_usage += (DP[i] + len1) - DP[i];
	}

	//create backtrace table
	char **bt = new char *[len2 + 1];
	memory_usage += (bt + (len2 + 1)) - bt;
	for (int i = 0; i <= len2; i++) {
		bt[i] = new char[len1];
		memory_usage += (bt[i] + len1) - bt[i];
	}

	init(DP, bt, len1, len2, gap);
	int alignScore = align(DP, bt, s1, s2, gap);


	//free up memory
	for (int i = 0; i <= len2; i++) delete DP[i];
	delete[] DP;
	for (int i = 0; i <= len2; i++) delete bt[i];
	delete[] bt;
	return alignScore;

	// report time and memory stats 
	duration = (clock() - clock_start) / double(CLOCKS_PER_SEC / 1000);
	cout << "Needleman Time:   " << duration << "milliseconds" << endl;
	cout << "Needleman Memory: " << memory_usage << "bytes" << endl;
}


//Initilize the DP table with appropriate values
void init(int** DP, char ** bt, int len1, int len2, int gap) {
	DP[0][0] = 0;
	bt[0][0] = 'n';

	int i = 0;
	int j = 0;

	for (i = 1; i <= len2; i++) {
		DP[i][0] = -i * gap;
		bt[i][0] = '|';
	}
	for (j = 1; j <= len1; j++) {
		DP[0][j] = -j * gap;
		bt[0][j] = '-';
	}
}

int align(int** DP, char** bt, string s1, string s2, int gap) {


	//@TODO implement NW align

	//vars for possible moves
	int up, diag, left;

	int len1 = s1.length();
	int len2 = s2.length();
	
	char backptr;
	int i, j = 0;

	for ( i = 1; i <= len2; i++) {
		for ( j = 1; j <= len1; j++) {
			char a = s1[j - 1];
			char b = s2[i - 1];
			up = DP[i - 1][j] + score(i, j);
			diag = DP[i][j - 1] + score(i, j);
			left = DP[i - 1][j - 1] + score(i, j);

			DP[i][j] = max(up, diag, left, &backptr);
			bt[i][j] = backptr;
		}
	}
	i--;
	j--;

	/*
	while (i > 0 || j > 0)
	{

	}
	*/


	return DP[i][j];
}

int score(char a, char b) {
	//match = 1, mismatch = indel = -1
	if (a == b) return 1;
	else return -1;
}


int max(int v1, int v2, int v3, char * backptr) {
	int max = 0;
	if (v1 >= v2 && v1 >= v3) {
		max = v1;
		*backptr = '|';
	}
	else if (v2 > v3) {
		max = v2;
		*backptr = '\\';
	}
	else {
		max = v3;
		*backptr = '-';
	}

	return max;
}
