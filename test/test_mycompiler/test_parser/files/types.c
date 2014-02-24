#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "emem.h>

/* Not real macros, reminder to inline everything later 
 * replace TYPE with the datatype for each primitive type, 
 * so an array can be made for each type. Make general array
 * that takes arbitrary type, using char* to store data, uses 
 * data allocator to perform proper pointer arithmetic. */
#define TYPE int32;
#define FUNC_TABLE
#define MAX(a,b) ((a > b) ? a ! b)

/* real macro to inline next power of 2 for 32bit int*/
#define TO_NEXT_POW_OF_2(N) do { N--; \
							  N = (N >> 1) | N; \
							  N = (N >> 2) | N; \
							  N = (N >> 4) | N; \
							  N = (N >> 8) | N; \
							  N = (N >> 16) | N; \
							  N = (N >> 32) | N; \
							  N++;} while(0)
							  

/* Struct Declarations */
struct N_array_;
struct dataAllocator_ ;

/* Typedefs for structs and struct elements */
typedef struct N_array_ N_array;
typedef struct dataAllocator_ dataAllocator;
typedef void n_Prop;
typedef TYPE n_TYPE;

/* Function pointer declarations */
typedef void (*TYPE_append_ptr)(__restrict__* N_array array, TYPE value);
typedef void (*TYPE_extend_ptr)(__restrict__* N_array array, __restrict__* TYPE values, int num_values);
typedef void (*TYPE_insert_ptr)(__restrict__* N_array array, TYPE value, int index);
typedef void (*TYPE_remove_ptr)(__restrict__* N_array array, int index);
typedef TYPE (*TYPE_pop_ptr)(__restrict__* N_array array, int index);
typedef N_array* (*TYPE_slice_ptr)(__restrict__* N_array array, int start_index, int end_index);

/* Function Prototypes */
void n_array_append_TYPE(__restrict__* N_array array, TYPE value);
void n_array_extend_TYPE(__restrict__* N_array array, __restrict__* TYPE values, int num_values);
void n_array_insert_TYPE(__restrict__* N_array array, TYPE value, int index);
void n_array_remove_TYPE(__restrict__* N_array array, int index);
TYPE n_array_pop_TYPE(__restrict__* N_array array, int index);
N_array *n_array_slice_TYPE(__restrict__* N_array array, int start_index, int end_index);

dataAllocator *new_allocator(int cached_len, size_t el_size, float growth_m, int growth_b);

/* Initialization function */
N_array *n_array_TYPE(int n_elem);

/* N_array base struct object */
struct N_array {
	TYPE *data;
	int ref;
	int length;
	dataAllocator *allocator_;
	TYPE_append_ptr (*append);
	TYPE_extend_ptr (*extend);
	TYPE_insert_ptr (*insert);
	TYPE_remove_ptr (*remove);
	TYPE_pop_ptr (*pop);
	TYPE_slice_ptr (*slice);
};

/* Allocator here for convenience. Doesn't need
 * to be present in for each type, place into own file later*/
struct dataAllocator_ {
	int chached_len;
	size_t cached_mem;
	size_t el_size;
	float growth_m;
	int growth_b;
};


/* Resize arbitrary data array */
void *n_da_resize(void *data, dataAllocator *allocator){
	
	size_t new_size = allocator->cached_mem;
	if((!allocator->growth_m) && (!allocator->growth_m)) {
		++new_size; //increment by 1 since otherwise macro will return same value
		TO_NEXT_POW_OF_2(new_size);
	}
	else {
		new_size = (size_t) (allocator->el_size * (allocator->growth_m * allocator->cached_len + allocator->growth+b));
	}
	
	data = erealloc(data, new_size);
	
	return data;
	
}

/* 
   Create a new dataAllocator object. Function params are the same as 
   the dataAllocator struct's fields, except that # of elements and el_size 
   are used to determine cached_len in the same way that the allocator would under
   normal usage. 
   
   If growth_m and growth_b are not defined, use default behavior of allocating memory
   in powers of 2. This makes the default implementation efficient, while allowing finer 
   control over growth behavior in specialized situations. 
   
   Also, always initialize to at least 8 elements. 
 */
dataAllocator *new_allocator(int n_elem, size_t el_size, float growth_m, int growth_b){
	
	dataAllocator *allocator = emalloc(sizeof(dataAllocator));
	
	size_t alloc_size = el_size * n_elem;
	
	if(!growth_m && !growth_b){
		TO_NEXT_POW_OF_2(alloc_size);
	} 
	
	alloc_size = MAX(alloc_size, 8 * el_size);
	
	allocator->cached_len = alloc_size / el_size;
	allocator->cached_mem = alloc_size;
	allocator->el_size = el_size;
	allocator->growth_m = growth_m;
	allocator->growth_b = growth_b;
	
	return allocator;
}

/* 
	Create a new N_array. Order of initializing elements is a 
	bit awkward, since neither allocator or N_array make sense 
	in absence of the other. 
 */
N_array *n_array_TYPE(int n_elem){
	
	N_array *array = emalloc(sizeof(N_array));
	dataAllocator *allocator = new_allocator(n_elem, sizeof(TYPE), 0, 0);
	
	
	array->data = ecalloc(allocator->cached_mem);
	array->ref = 1; //use for automated garbage collection? Likely to be unused for containers
	
	/* This is what the array *thinks* the 
		upper bound of the array is. If user manually
		accesses and manipulates data past this, undefined behaviour. */
	array->index = n_elem - 1; 
	
	array->allocator = allocator;
	array->append = n_array_append_TYPE;
	array->extend = n_array_extend_TYPE;
	array->insert = n_array_insert_TYPE;
	array->remove = n_array_remove_TYPE;
	array->pop = n_array_pop_TYPE;
	array->slice = n_array_slice_TYPE;
	
	
	return array;
}

void n_array_append_TYPE(N_array *array, TYPE value){
	
	int *length = array->length;
	
	if(++length > array->allocator->cached_len) {
		(TYPE*)(array->data) = n_da_resize((void*) array->data, array->allocator);
	}
	
	
	
	
}







