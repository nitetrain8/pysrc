
#ifndef MKPATH_H_
#define MKPATH_H_

#define MKPATH_NULL_PATH -1
#define MKPATH_NULL_DIR -2
#define MKPATH_NEED_UP -3
#define MKPATH_MKDIR_ERROR -4
#define MKPATH_ERROR -5
#define DIR_SEP_CHAR '\\'
#define DIRNAME_MAX_PATH MAX_PATH
#define DIREND_NO_DIR -1
#include <sys/stat.h>

#ifndef MAX_PATH
#define MAX_PATH 260
#endif


int dirname(const char * __restrict__ path, char * pdir);
int mkpath(const char * __restrict__ path);

#endif //MKPATH_H_