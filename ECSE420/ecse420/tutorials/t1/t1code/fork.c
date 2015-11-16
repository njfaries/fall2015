
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{

  pid_t fork(void);
  pid_t pid, child_pid, parent_pid;

  switch (pid = fork())
  {
    case -1:
	perror("The fork failed!");
	break;

    case 0:
	child_pid = getpid();
	printf("\nHello I am a new Child w/ PID %d\n",child_pid);
	break;

    default:
	parent_pid = getpid();
	printf("\nHello I am parent w/ PID %d and\nI created the process %d\n",parent_pid, pid);
    }

  return 0;
}


