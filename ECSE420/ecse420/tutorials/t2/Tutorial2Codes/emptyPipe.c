
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{

  pid_t fork(void);
  pid_t pid, child_pid, parent_pid;

  int fd[2];
  int n1, n2;
  pipe(fd);


  // this is an example to show that processes stall while 
  // reading at the reading end of an empty pipe. 

  switch (pid = fork())
  {
    case -1:
	perror("The fork failed!");
	break;

    case 0:
	child_pid = getpid();
	printf("\nHello I am a new Child w/ PID %d\nand will receive a token from my father\n",child_pid);
	read(fd[0], &n2, sizeof(n2));
	printf("--->I received %d\n", n2);
	break;

    default:
	parent_pid = getpid();
	printf("\nHello I am parent w/ PID %d and\nI will send a token \"n1=%d\" to my child process %d\n",parent_pid, n1, pid);
        int n1 = 0;
	// let's add a busy wait to delay the message
        sleep(5); 
	write(fd[1], &n1, sizeof(n1));
    }

  return 0;
}


