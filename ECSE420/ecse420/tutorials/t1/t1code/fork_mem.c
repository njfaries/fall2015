
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{

  pid_t pid, child_pid;
  int a[10]= {0,10,20,30,40,50,60,70,80,90};
  int i;

  switch (pid = fork())
  {
    case -1:
	perror("The fork failed!");
	break;

    case 0:
	child_pid = getpid();
	printf("Hello I am a new Child's my pid is %d\n",child_pid);
	a[4]= 50;
	break;

    default:
	printf("Hello I am parent I just created a new process %d\n",pid);
	a[4]= 30;
    }

    for ( i = 0; i < 10; i++)
	printf("a[%d]=%d\n", i , a[i]);

  return 0;
}


