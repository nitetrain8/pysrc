#include <sys/stat.h>
#include <string.h>
#include <fcntl.h>
#include "mkpath.h"
#include <errno.h>
#include <stdlib.h>
#define MKPATH_DEBUG


#ifdef MKPATH_DEBUG
#include <stdio.h>
#include "sigecho.h"
#endif //MKPATH_DEBUG

int mkpath(const char * __restrict__ path){
	char dir[] = {[0 ... MAX_PATH - 1] = 0};
	int rv; 
#ifdef MKPATH_DEBUG
	static int depth = 0;
	if ((++depth) > 10){
		exit(-1);
	}
#endif
	
	
	//null path -> abort
	if (path == NULL){ 
		rv = MKPATH_NULL_PATH;
		goto leave;
	}
	
	if((strcmp(path, ".") == 0) || // ignore error prone names/hidden dirs
	   (strcmp(path, "..") == 0) || 
	   (strcmp(path, "/") == 0) || 
	   (strcmp(path, "\\") == 0)){
	   rv = 0;
	   goto leave;
	   
	}

	if(dirname(path, dir) == DIREND_NO_DIR){
		rv = MKPATH_NULL_PATH;
		goto leave;
	} 

#ifdef MKPATH_DEBUG
	printf("MKPATH DEBUG PATH: %s\n", path);

	printf("MKPATH DEBUG DIR: %s\n", dir);
#endif //MKPATH_DEBUG
	
	if((mkpath(dir) != 0) && errno != EEXIST){
		rv = MKPATH_MKDIR_ERROR;
		goto leave;
	}
	
	if ((mkdir(path) == -1) && (errno != EEXIST)){
		rv = MKPATH_MKDIR_ERROR;
	} else {
		rv = 0;
	}
	
	leave:
		//free(dir); //initialized to NULL, safe to free
#ifdef MKPATH_DEBUG
		printf("MKPATH return value: %d\n", rv);
#endif //MKPATH_DEBUG
		return rv;
	
}

//#define DIRNAME_DEBUG
 inline int dirname(const char* __restrict__ path, char * pdir){

	char * dirend = strrchr(path, DIR_SEP_CHAR);
	if(dirend == NULL){
		return DIREND_NO_DIR;
	}
	size_t len = dirend-path;
#ifdef DIRNAME_DEBUG
	strncpy(pdir, path, ((len > MAX_PATH) ? MAX_PATH : len)); // use ternary if dirend == null and len is huge 
#else
	strncpy(pdir, path, len);
#endif //DIRNAME_DEBUG
	//*(pdir + len + 1) = '\0';
	
	return 0;
	
}

#ifdef MKPATH_DEBUG
#define SOLO
#ifdef SOLO

int main(int argc __attribute__ ((unused)), char ** argv __attribute__ ((unused))){

#ifdef SIG_ECHO_H
	set_sig_echo();
#endif //SIG_ECHO_H

    char src[] = "C:\\Users\\Administrator\\Csrc\\pbsbkup\\ctsrc\\level2";
	mkpath(src);

	return 0;
}
#endif //SOLO



#endif //MKPATH_DEBUG
