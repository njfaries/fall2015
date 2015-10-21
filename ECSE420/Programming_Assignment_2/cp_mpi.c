#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>

#define MASTER_TO_SLAVE_TAG 1 //tag for messages sent from master to slaves
#define SLAVE_TO_ANY_TAG 2
#define SLAVE_TO_MASTER_TAG 4 //tag for messages sent from slaves to master

//each process takes rows (size * i) + rank

int rank, size, numrows, numcols, current_pivot;
double ** matrix, ** final_matrix;
MPI_Status status;
MPI_Request request;

/*
Code to allocate the matrix copied from cp_sequential.c and slightly modified
*/

double ** allocate_matrix(int rows, int cols)
{
	int i;
	double ** matrix = (double **) malloc((rows + 1) * sizeof(double *));

	for (i = 0; i < rows; i++) {
		matrix[i] = (double *) malloc(cols * sizeof(double));
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

void print_matrix(double ** matrix, int rows, int cols) 
{
	int row, column;
	for (row = 0; row < rows; row++) {
	 	for (column = 0; column < cols; column++) {
	 		printf("%lf ",matrix[row][column]);
	 	}
	 	printf("\n");
	}	
}

void do_elimination(double ** matrix, double * received_row, int * current_pivot)
{
	int i, j;
	double coefficient;
	for (i = 0; i < numrows; i++) {
		if (!(((*current_pivot % size) == rank) && (*current_pivot / size) == i)) {
			if (received_row[*current_pivot] != 0) {coefficient =  matrix[i][*current_pivot] / received_row[*current_pivot];}
			for (j = 0; j < numcols; j++) {
				matrix[i][j] -= received_row[j] * coefficient;
			}
		}
	}
}

void absolute(double ** matrix, int * rows, int * cols)
{
	int i, j;
	for (i = 0; i < *rows; i++) {
		for (j = 0; j < *cols; j++) {
			matrix[i][j] = fabs(matrix[i][j]);
		}
	}
}

double getmax(double ** matrix, int * rows, int * cols)
{
	int i;
	double max;
	for (i = 0; i < *rows; i++) {
		if (matrix[i][*cols - 1] > max) { max = matrix[i][*cols - 1];}
	}
	return max;
}

void RREF(double ** matrix)
{
	int i;
	while (current_pivot < numcols - 1){
		MPI_Barrier(MPI_COMM_WORLD);
		if ((current_pivot % size) == rank) {
			//my turn to send out information!
			//sending row current_pivot/size
			if (matrix[current_pivot/size][current_pivot] < 0) {
				int j;
				for (j = 0; j < numcols; j++) {
					matrix[current_pivot/size][j] = -matrix[current_pivot/size][j];
				}
			}
			for (i = 0; i < size; i++) {
				// printf ("current_pivot is %d and matrix[cp][cp] is %lf\n", current_pivot, matrix[current_pivot/size][current_pivot]);
				MPI_Send(matrix[current_pivot/size], numcols, MPI_DOUBLE, i, SLAVE_TO_ANY_TAG, MPI_COMM_WORLD);
			}
			do_elimination(matrix, matrix[current_pivot/size], &current_pivot);
		} else {
			//receive from process #(current_pivot % size)
			double received_row[numcols];
			MPI_Recv(&received_row, numcols, MPI_DOUBLE, (current_pivot % size), SLAVE_TO_ANY_TAG, MPI_COMM_WORLD, &status);
			// for (i = 0; i < numcols; i++) {
			// 	printf("Value %d in row is %lf received by process %d and the pivot is %d\n", i, received_row[i], rank, current_pivot);
			// }
			do_elimination(matrix, received_row, &current_pivot);
		}
		MPI_Barrier(MPI_COMM_WORLD);
		current_pivot++;
	}
}

void reduction(double ** matrix, int * rows, int * cols)
{
	double max = 0;
	int i, j;
	if (rank == 0) { //master
		max = getmax(matrix, rows, cols);
		double temp;
		for (i = 1; i < size; i++) { //get the max from each other process
			MPI_Recv(&temp, 1, MPI_DOUBLE, i, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD, &status);
			if (temp > max) {max = temp;}
		}
	} else { //slave
		max = getmax(matrix, rows, cols);
		MPI_Send(&max, 1, MPI_DOUBLE, 0, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD);
	}
	MPI_Barrier(MPI_COMM_WORLD);
	if (rank == 0) { //master
		for (i = 1; i < size; i++) {
			MPI_Isend(&max, 1, MPI_DOUBLE, i, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &request);
		}
	} else { //slave
		MPI_Recv(&max, 1, MPI_DOUBLE, 0, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &status);
	}
	for (i = 0; i < *rows; i++) {
		for (j = 0; j < *cols; j++) {
			matrix[i][j] /= max;
		}
	}
}

void collect(double ** matrix)
{
	int i;
	if (rank == 0) { //master
		final_matrix = allocate_matrix((numcols - 1), numcols);
		for (i = 0; i < (numcols - 1); i++) {
			if ((i % size) == rank) {
				final_matrix[i] = matrix[i/size];
			} else {
				MPI_Recv(final_matrix[i], numcols, MPI_DOUBLE, (i % size), SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD, &status);
			}
		}
	} else { //slave
		for (i = 0; i < numrows; i++) {
			MPI_Send(matrix[i], numcols, MPI_DOUBLE, 0, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD);
		}
	}
}

void output_to_file(double ** matrix)
{
	int i, j;
	FILE *file;
	file = fopen("clicking_probabilities.txt", "w");
	for (i = 0; i < numcols - 1; i++) {
		char str[80]; //arbitrary to make sure it's long enough
		sprintf(str, "%lf\n", final_matrix[i][numcols - 1]);
		fputs(str, file);
	}
	fclose(file);
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
	matrix = allocate_matrix(numrows, numcols);
	read_rows(argv[1], matrix);
	RREF(matrix);
	absolute(matrix, &numrows, &numcols);
	reduction(matrix, &numrows, &numcols);
	collect(matrix);
	if (rank == 0) {
		print_matrix(final_matrix, numcols - 1, numcols);
		output_to_file(final_matrix);
	}
	free_matrix(matrix, &numrows);
	ierr = MPI_Finalize();
}