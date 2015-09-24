#include <stdio.h>
#include <time.h>
#include <pthread.h>


int string_mutex = 0;
int mutex = 0;
int varying_int = 5;

void * thread_function(void* arg)
{
	while (mutex == 1);	
	mutex = 1;
	while (string_mutex == 1);
	string_mutex = 1;
	mutex = 0;
	varying_int = varying_int + 1;
	printf("%d", varying_int);
	string_mutex = 0;
	return NULL;
}

void * subtract(void* arg)
{
	while (mutex == 1);
	mutex = 1;
	while (string_mutex == 1);
	string_mutex = 1;
	mutex = 0;
	varying_int = varying_int - 1;
	printf("%d", varying_int);
	string_mutex = 0;
	return NULL;
}

int main(int argc, char* argv) 
{
	int i;
	for (i = 0; i < 5; i++)
	{
		pthread_t thread;
		pthread_create(&thread, NULL, thread_function, NULL);
		pthread_join(thread, NULL);
	}

	for (i = 0; i < 10; i++)
	{
		pthread_t minus;
		pthread_create(&minus, NULL, subtract, NULL);
		pthread_join(minus, NULL);
	}

	return 0;
}