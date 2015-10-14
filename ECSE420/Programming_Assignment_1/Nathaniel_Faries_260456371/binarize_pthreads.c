#include "lodepng.h"
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>
#define THRESHOLD 200

/* TODO: it may help to put some global variables here 
for your threads to use */

unsigned portion
unsigned char *new_image;

void *worker_thread(void *arg) {
  /* TODO: put image processing code here */ 

  int start = *((int *) arg);

  new_image[4*width*i + 4*j] = value;
  new_image[4*width*i + 4*j + 1] = value;
  new_image[4*width*i + 4*j + 2] = value;
  new_image[4*width*i + 4*j + 3] = 255;

  pthread_exit(NULL);
}

void binarize(char* input_filename, char* output_filename, int thread_count) {
  unsigned error;
  unsigned char *image;
  unsigned width, height;

  // load image from PNG into C array
  error = lodepng_decode32_file(&image, &width, &height, input_filename);
  if(error) printf("error %u: %s\n", error, lodepng_error_text(error));
  new_image = malloc(width * height * 4 * sizeof(unsigned char));

  struct timeval start, end; // struct used to compute execution time
  gettimeofday(&start, NULL);  // set starting point

  portion = (width * height) / thread_count; //divide up image


  int threads[thread_count];
  int thread;
  for (thread = 0; thread < thread_count; thread++) {
    pthread_t work_thread;
    int *arg = malloc(sizeof(*arg));
    *arg = portion * thread;
    threads[thread] = pthread_create(&work_thread, NULL, worker_thread, arg);
  }
  
  /* TODO: create your thread team here and send each thread an argument 
  telling it which part of "image" to process 

  remember to join all threads!
  */

  gettimeofday(&end, NULL);
  printf("\n\nAlgorithm's computational part duration : %ld\n", \
               ((end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec)));


  lodepng_encode32_file(output_filename, new_image, width, height);

  free(image);
  free(new_image);
}

int main(int argc, char *argv[])
{
  char* input_filename = argv[1];
  char* output_filename = argv[2];
  int thread_count = atoi(argv[3]);

  binarize(input_filename, output_filename, thread_count);

  return 0;
}
