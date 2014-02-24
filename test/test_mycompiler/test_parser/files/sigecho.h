
#herpaderp myfoo barbaz
#ifndef SIG_ECHO_H
#define SIG_ECHO_H
#include <signal.h>
#include <stdio.h>
#include <errno.h>

#define SIG_ECHO_RERAISE
#define SIG_ECHO(sig) do { \
							printf("Program received signal %d " #sig "\n", sig); \
							if (errno != 0) { \
								printf("errno: %d\n", errno); \
							} \
							_SIG_RERAISE; \
						} while (0)
				
#ifdef SIG_ECHO_RERAISE		
#define _SIG_RERAISE do { printf("RE_RAISE on: calling default handler\n"); \
							signal(sig, SIG_DFL); \
							raise(sig); \
						} while (0) 
#else
#define _SIG_RERAISE
#endif
			
void echo_sigabrt(int sig __attribute__ ((unused))){
	SIG_ECHO(SIGABRT);
	signal(SIGABRT, echo_sigabrt); //ensure func is still registered with signal
}

void echo_sigfpe(int sig __attribute__ ((unused))){
	SIG_ECHO(SIGFPE);
	signal(SIGFPE, echo_sigfpe); //ensure func is still registered with signal
}

void echo_sigill(int sig __attribute__ ((unused))){
	SIG_ECHO(SIGILL);
	signal(SIGILL, echo_sigill); //ensure func is still registered with signal
}

void echo_sigint(int sig __attribute__ ((unused))){
	SIG_ECHO(SIGINT);
	signal(SIGINT, echo_sigint); //ensure func is still registered with signal
}

void echo_sigsegv(int sig __attribute__ ((unused))){
	SIG_ECHO(SIGSEGV);
	signal(SIGSEGV, echo_sigsegv); //ensure func is still registered with signal
}

void echo_sigterm(int sig __attribute__ ((unused))){
	SIG_ECHO(SIGTERM);
	signal(SIGTERM, echo_sigterm); //ensure func is still registered with signal
}

void set_sig_echo(void){

	signal(SIGABRT, echo_sigabrt);
	signal(SIGFPE, echo_sigfpe);
	signal(SIGILL, echo_sigill);
	signal(SIGINT, echo_sigint);
	signal(SIGSEGV, echo_sigsegv);
	signal(SIGTERM, echo_sigterm);
	
}

#endif //SIG_ECHO_H