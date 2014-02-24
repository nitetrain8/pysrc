#include "copytree.h"
#include <windows.h>
#include <stdio.h>
#include "mkpath.h"
#include <sys/stat.h>


#define CTDEBUG
//#undef CTDEBUG
	
							
int copytree(const char * __restrict__ src, const char * __restrict__ dst){

#ifdef CTDEBUG

#ifdef DEBUGSPRINTF
#define sprintf(buf, fmt, args...) do { sprintf(buf, fmt, args); \
									printf("Func: %s\nLine: %d\nbuf: %s\n\n", __PRETTY_FUNCTION__, __LINE__, buf); \
									} while(0)
#endif //DEBUGSPRINTF

#define copytree(src, dst) do { printf("dst: %s\n", dst); \
								printf("src: %s\n", src); \
								copytree(src, dst); \
							} while(0)
#undef CopyFile
#define CopyFile(src, dst, bFail) do { printf("src: %s\n", src); \
								printf("dst: %s\n", dst); \
								}while(0)
#endif //CTDEBUG
	int bMkpath;
	if( (bMkpath = mkpath(dst)) != 0){
#ifdef CTDEBUG
		printf("%d", bMkpath);
		printf("%d", errno);
#endif //CTDEBUG
		return bMkpath;

	}

	char sPath[MAX_PATH];
	char dPath[MAX_PATH];
	HANDLE fHandle;
	WIN32_FIND_DATA fInfo;
	
	sprintf(sPath, "%s\\*", src);
	
	
	fHandle = FindFirstFile(sPath, &fInfo);
	
	if(INVALID_HANDLE_VALUE == fHandle){
		return -1;
	}
	
	do {
		if((strcmp(fInfo.cFileName, ".") != 0) && (strcmp(fInfo.cFileName, "..") != 0)){
			sprintf(sPath, "%s\\%s", src, fInfo.cFileName);
			sprintf(dPath, "%s\\%s", dst, fInfo.cFileName);
			
			if(fInfo.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY){ 
				//dir, call recursively with built path
				//eventually this will fall through all the way
				//copytree(sPath, dPath);
				
			} else { 
				//not a directory, copy file
				CopyFile(sPath, dPath, 0);
			}

		
		}
	} while (FindNextFile(fHandle, &fInfo));
	
	FindClose(fHandle);
		
	return 0;
}

#ifdef CTDEBUG
int main(int argc, char** argv) {

	char *src;
	char *dst;
	if(argc == 1){
		src = "C:\\Users\\Administrator\\Csrc\\pbsbkup\\ctsrc";
		dst = "C:\\Users\\Administrator\\Csrc\\pbsbkup\\ctsrc";
	} else {
		src = argv[1];
		dst = argv[2];	
	}
	copytree(src, dst);

	return 0;
}
#endif 

#ifdef CTDEBUG
#undef CTDEBUG
#endif

#ifdef DEBUGSPRINTF
#undef DEBUGSPRINTF
#endif








