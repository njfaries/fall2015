#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "math.h"

#define MASTER_TO_SLAVE_TAG 1 //tag for messages sent from master to slaves
#define SLAVE_TO_MASTER_TAG 4 //tag for messages sent from slaves to master

//each process takes rows (size * i) + rank

int rank, size, numrows, numcols, max_i;
MPI_Status status;
MPI_Request request;


void get_number_of_rows(char* filename, int* rows)
{
	FILE *file;
	file = fopen(filename, "r");
	*rows = 1;
	char c;
	while(!feof(file)) {
		c = fgetc(file);
		if (c == '\n') {
			(*rows)++;
		}
	}
}

double ** read_rows(char* filename)
{
	FILE *file;
	file = fopen(filename, "r");
	int newline_count = 0;
	int iteration = 0;
	int size = 0;
	while (!feof(file)) {
		while (newline_count < rank && !feof(file)) {
			c = fgetc(file);
			if (c == '\n') {
				newline_count++;
			}
		}
	}
}


int main(int argc, char * argv[])
{
	if (argc != 2) {printf("Please provide a matrix");}

	int ierr = MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); //sets rank
	MPI_Comm_size(MPI_COMM_WORLD, &size); //gets number of processes

	if (rank == 0) { //master process
		get_number_of_rows(argv[1], &numrows);
		numcols = numrows + 1; //specified by assignment
		max_i = numrows / size; //maximum iteration of distributing rows among the processes, inclusive
		int i;
		for (i = 1; i < size; i++) { //sending out information to slaves about what rows they are reading.
			printf("Sending to %d\n", i);
			MPI_Isend(&numrows, 1, MPI_INT, i, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &request);
		}
	}
	else {
		MPI_Recv(&numrows, 1, MPI_INT, 0, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &status);
		numcols = numrows + 1;
		printf("Process %d received %d from master\n", rank, numrows);
	}
	ierr = MPI_Finalize();
}