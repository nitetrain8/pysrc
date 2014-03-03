#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

char *cellstr(long number);

int main(int argc, char *argv[]) {

	//get number from somewhere
	int i;
	for(i = 0; i < 1000; i++){
		printf("%s", cellstr( (long) number), 1);
	}
	
	return 0;

}

char *cellstr(long row, long col){

	int numdig = 1; 
	long startsum = 26;
	
	/*get number of digits by checking value of col vs adding 
	 *powers of 26 in succession
	 */
	for(numdig = 1; col > startsum; numdig++){
		startsum += pow(26,numdig)	
	}
	
	/*initialize array to hold string. extra space for '\0' */
	char *cellstring[numdig+1];
	cellstring[numdig] = '\0';
	
	/*since no type conversion in C, need separate
	 *array to hold numbers for calculation
	 */
	long *cellnum[numdig];
	cellnum[0] = col;
	
	int i;
	int exp;
	
	/*Base excel algorithm! should be the same as python version
	 *but uses zero based index on i instead of 1 based, makes adjustment
	 *on inner loop indexes. Should be no performance change. 
	 *Same strategy: iterate over all digits, subtracting as big of a 
	 *power of power of 26 as possible. Biggest exp to subtract 
	 *is numdig-i-1, since a power is lost each time you move up
	 *a digit.
	 */
	 
	for(i = 0; ++i < numdig;){
		
		for(exp = numdig-i-1; exp > 1; --exp) {
			
			while(cellnum[i] > pow(26,exp) {
		
				cellnum[i] -= pow(26,exp);
				cellnum[i+1] += pow(26,exp-1);
				
			}
		}
	
	}
	
	for(i = 0; ++i < numdig;){
		cellstring[i] = chr(64 + (int)cellnum[i]);
	}

	
	return cellstring;
}
