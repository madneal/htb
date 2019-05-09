#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
	setuid(1000, 1000);
	printf("ID: %d\n", getuid());
	execve("/bin/sh", NULL, NULL);
}
