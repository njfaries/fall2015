#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <string.h>

char global_string[10000];
pthread_mutex_t thread_mutex;

void * thread_function(void* arg)
{
	int id = *((int *) arg);
	struct timespec t, s;
	int micro = (rand() % 1000) * 1000;
	t.tv_sec = 0;
	t.tv_nsec = micro;
	// printf("Hi there.  I'm thread %d\n", id);
	// printf("Thread %d sleeping for %d nanoseconds\n", id, micro);
	char string[10];
	sprintf(string, "%d, ", id);
	nanosleep(&t, &s);
	pthread_mutex_lock(&thread_mutex);
	strcat(global_string, string);
	printf("%s\n", global_string);
	pthread_mutex_unlock(&thread_mutex);
	// printf("Thread %d is awake!\n", id);
	free(arg);
	pthread_exit(0);
}

void forking(int numthreads)
{
	int i;
	int threads[numthreads];
	for(i = 0; i < numthreads; i++) {
		pthread_t thread;
		// printf("Spawning thread %d\n", i);
		int *arg = malloc(sizeof(*arg));
		*arg = i;
		threads[i] = pthread_create(&thread, NULL, thread_function, arg);
	}	
}

int main(int argc, char* argv[])
{
	srand(time(NULL)); // initialize random seed
	pthread_mutex_init(&thread_mutex, NULL);
	int numthreads;
	if (argc != 2 || (numthreads = atoi(argv[1])) == 0 || numthreads > 100) { //capped to prevent things from exploding.
		printf("Enter a valid number!");
		return 0;
	}
	forking(numthreads);

	pthread_exit(0);
	printf("Test\n");
	printf("%s", global_string);
}
