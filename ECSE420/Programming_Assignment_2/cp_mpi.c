#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "math.h"

#define MASTER_TO_SLAVE_TAG 1 //tag for messages sent from master to slaves
#define SLAVE_TO_ANY_TAG 2
#define SLAVE_TO_MASTER_TAG 4 //tag for messages sent from slaves to master

//each process takes rows (size * i) + rank

int rank, size, numrows, numcols, current_pivot;
double ** matrix;
MPI_Status status;
MPI_Request request;

/*
Code to allocate the matrix copied from cp_sequential.c and slightly modified
*/

double ** allocate_matrix(int* rows, int* cols)
{
	int i;
	double ** matrix = (double **) malloc((*rows + 1) * sizeof(double *));

	for (i = 0; i < *rows; i++) {
		matrix[i] = (double *) malloc(*cols * sizeof(double));
	}

	return matrix;
}

/*
Code to free matrix copied from cp_sequential.c
*/

void free_matrix(double ** matrix, int* rows)
{
	int i;
	for (i = 0; i < *rows; i++) free(matrix[i]);
	free(matrix);
}

/*
Code to get the number of rows copied from cp_sequential.c
*/

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

void advance_number_of_rows(FILE *file, int rows)
{
	char c;
	int i = 0;
	while(!feof(file) && i < rows) {
		c = fgetc(file);
		if (c == '\n') {
			i++;
		}
	}
}

void enter_line_into_matrix(char * line, int row)
{
	int i;
	double value;
	for (i = 0; i < numcols; i++) {
		value = strtod(line, &line);
		matrix[row][i] = value;
	}

}

void read_rows(char* filename, double ** matrix)
{
	FILE *file;
	file = fopen(filename, "r");
	int newline_count = 0;
	int iteration = 1;
	size_t linesize = 0;
	char * line;
	advance_number_of_rows(file, rank);
	getline(&line, &linesize, file);
	enter_line_into_matrix(line, 0);
	while (iteration < numrows) {
		advance_number_of_rows(file, size - 1); //size minus one since you've already moved the pointer up one line by reading it.
		linesize = 0;
		getline(&line, &linesize, file);
		enter_line_into_matrix(line, iteration);
		iteration++;
	}
}

void print_matrix(int* rows, int* cols) 
{
	int row, column;
	for (row = 0; row < *rows; row++) {
	 	for (column = 0; column < *cols; column++) {
	 		printf("%lf ",matrix[row][column]);
	 	}
	 	printf("\n");
	}	
}

void do_elimination(double ** matrix, double * received_row, int * current_pivot)
{
	int i, coefficient;
	for (i = 0; i < numrows; i++) {
		coefficient = received_row[*current_pivot] / matrix[i][*current_pivot];
	}
}

void RREF(double ** matrix)
{
	int i;
	while (current_pivot < numcols){
		if ((current_pivot % size) == rank) {
			for (i = 0; i < size; i++) {
				MPI_Isend(matrix[current_pivot/size], numcols, MPI_DOUBLE, i, SLAVE_TO_ANY_TAG, MPI_COMM_WORLD, &request);
			}
			//my turn to send out information!
			//sending row current_pivot/size
		} else {
			double received_row[numcols];
			//receive from process #(current_pivot % size)
			MPI_Recv(&received_row, numcols, MPI_DOUBLE, (current_pivot % size), SLAVE_TO_ANY_TAG, MPI_COMM_WORLD, &status);
			// for (i = 0; i < numcols; i++) {
			// 	printf("Value %d in row is %lf\n", i, received_row[i]);
			// }
			do_elimination(matrix, received_row, &current_pivot);
		}
		current_pivot++;
	}
}

int main(int argc, char * argv[])
{
	if (argc != 2) {printf("Please provide a matrix");}

	int ierr = MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); //sets rank
	MPI_Comm_size(MPI_COMM_WORLD, &size); //gets number of processes
	current_pivot = 0;

	if (rank == 0) { //master process
		get_number_of_rows(argv[1], &numrows);
		numcols = numrows + 1; //specified by assignment
		int i;
		for (i = 1; i < size; i++) { //sending out information to slaves about what rows they are reading.
			printf("Sending to %d\n", i);
			MPI_Isend(&numrows, 1, MPI_INT, i, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &request);
		}
	}
	else {
		MPI_Recv(&numrows, 1, MPI_INT, 0, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &status);
		numcols = numrows + 1;
	}
	if (rank >= numrows) {
		ierr = MPI_Finalize();
		return 0;
	} else if (rank < (numrows % size)) {
		numrows = (numrows / size) + 1;
	} else {
		numrows = (numrows / size);
	}
	printf("Process %d:\n", rank);
	matrix = allocate_matrix(&numrows, &numcols);
	read_rows(argv[1], matrix);
	print_matrix(&numrows, &numcols);
	RREF(matrix);
	free_matrix(matrix, &numrows);
	ierr = MPI_Finalize();
}