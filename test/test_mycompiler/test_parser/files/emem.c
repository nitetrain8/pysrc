#include <stdlib.h>
#include <stdio.h>



void log_mem_err(char *message){
	
	printf("Fatal error: %s\n", message);
	printf("Attempting to log error and quit application.\n");

	//log error if possible
}

void *emalloc(size_t size){
	
	void *ptr = malloc(size);
	if(!ptr) {
		log_mem_err("Failed to allocate %I64d bytes to heap.", size);
	}
	
	return ptr;
	
}

void *ecalloc(int blocks, size_t size){
	
	void *ptr = calloc(blocks, size);
	if(!ptr) {
		log_mem_err("Failed to allocate %d blocks of %I64d bytes to heap.", blocks, size);
	}
	
	return ptr;
	
}

void *erealloc(void *ptr, size_t size){
	
	void *temp_ptr = realloc(ptr, size);
	if(!temp_ptr) {
		log_mem_err("Failed to reallocate %I64d bytes to heap.", size);
	}
	else {
		free(ptr);
		ptr = temp_ptr;
		temp_ptr = NULL;
	}
	return ptr;
	
}