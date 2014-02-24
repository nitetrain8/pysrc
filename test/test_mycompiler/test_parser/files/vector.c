#include <stdlib.h>
#include "emem.h"

/* bit twiddle hacks from http://graphics.stanford.edu/~seander/bithacks.html  */
#define IS_POWER_OF_TWO(N) (N & (N - 1) == 0)
#define NEXT_POWER_OF_TWO(N) 

struct dataAllocator_;
struct ivector_;



typedef struct dataAllocator_ dataAllocator;
typedef struct ivector_ ivector;

void alloc_resize(char *vector);
void iv_append(ivector *vector, int value);
void iv_insert(ivector *vector, int value);
void iv_extend(ivector *vector, restrict* int values);
void iv_remove(ivector *vector, int index);
ivector new_ivector(int elements);


typedef void (*alloc_resize_ptr)(char *vector);
typedef void (*iv_append_ptr)(ivector* vector, int value);
typedef void (*iv_insert_ptr)(ivector* vector, int value);
typedef void (*iv_extend_ptr)(ivector* vector, restrict* int values);
typedef void (*iv_remove_ptr)(ivector* vector, int index);

struct dataAllocator_ {
	int cached_len_; 
	size_t element_size_;
	float growth_m_;
	int growth_b_;
	alloc_resize_ptr (*resize);
};

struct ivector_ {

	int index;
	iv_append_ptr (*append);
	iv_extend_ptr (*extend);
	iv_insert_ptr (*insert);
	iv_remove_ptr (*remove);
	
	dataAllocator *allocator;
	int array[0];
};

ivector *new_ivector(int elements){
	
	dataAllocator *allocator = emalloc(sizeof(dataAllocator));
	
	allocator->element_size_ = sizeof(int);
	allocator->growth_m_ = 1.25;
	allocator->growth_b_ = 5;
	allocator->resize = alloc_resize;
	
	
	size_t init_size = sizeof(ivector) + elements * sizeof(int);
	
	
	
	ivector *vector = emalloc(init_size);
	vector->index = -1;
	vector->extend = iv_extend;
	vector->insert = iv_insert;
	vector->append = iv_append;
	vector->remove = iv_remove;
	
	
	
	
	vector->allocator = allocator;
	
	return vector;
	
}

void iv_append(ivector *vector, int value){
	
	int *index = ivector->index;
	
	if(++index 
	
	
	
	
}

