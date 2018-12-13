#include <iostream>;
using namespace std;

int main() {
	H();
	NW();
	return 0;
}

//implementaiton of Hirshberg Alg.
void H() {
	return;
}


//implementaiton of Needleman-Wunsch Alg.
int NW(string s1, string s2) {

	//gap penalty
	int gap = 2;

	//sequence lengths
	int len1 = s1.length();
	int len2 = s2.length();

	//create DP table
	int **DP = new int *[len2 + 1];
	for (int i = 0; i <= len2; i++) {
		DP[i] = new int[len1];
	}

	//create backtrace table
	char **bt = new char *[len2 + 1];
	for (int i = 0; i <= len2; i++) {
		bt[i] = new char[len1];
	}

	init(DP, bt, len1, len2, gap);
	align(DP, bt, s1, s2, gap);


	//free up memory
	for (int i = 0; i <= len2; i++) delete DP[i];
	delete[] DP;
	for (int i = 0; i <= len2; i++) delete bt[i];
	delete[] bt;
	return 0;
}


//Initilize the DP table with appropriate values
void init(int** DP, char ** bt, int len1, int len2, int gap) {
	DP[0][0] = 0;
	bt[0][0] = 'n';

	int i = 0;
	int j = 0;

	for (i = 1; i <= len2; i++) {
		DP[i][0] = -i * gap;
		bt[i][0] = '-';
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
	
	for (int i = 1; i <= len2; i++) {
		for (int j = 1; j <= len1; j++) {

			up = DP[i-1][j] + score();
			diag = DP[i][j-1] + score();
			down = DP[i - 1][j - 1] + score();
		}
	}


	return 0;
}

int score(char a, char b) {

}