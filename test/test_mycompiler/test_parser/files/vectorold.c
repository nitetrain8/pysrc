#include <stdio.h>
#include <stdlib.h>


struct _vector;

typedef struct _vector vector;
typedef int (*append_ptr)(*vector, *void);
typedef int (*extend_ptr)(*vector);

int v_append(*vector vector, void *value);
int v_extend(*vector vector);

typedef struct _vector{
	void *array;
	int el_max;
	int current;
	size_t el_size;
	float growth_m;
	int growth_b;
	char *type;
	append_ptr *append;
	extend_ptr *extend;
} vector;










int main(int argc, char *argv[], **envp){



	return 0;
}