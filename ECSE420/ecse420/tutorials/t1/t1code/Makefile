all: fork fork_mem wait thread_create thread_join

fork: fork.c
	gcc -o fork fork.c 

fork_mem: fork_mem.c
	gcc -o fork_mem fork_mem.c 

wait: wait.c
	gcc -o wait wait.c 

thread_create: thread_create.c
	gcc -o thread_create  -pthread  thread_create.c 

thread_join: thread_join.c
	gcc -o thread_join  -pthread  thread_join.c 





