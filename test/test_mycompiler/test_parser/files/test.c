#include <stdio.h>

int main (int argc, char ** argv, char ** env){

	char bob[20];
	
	for(int i = 0; i < 20; ++i){
		printf("%d", bob[i]);
	}

	return 0;
}