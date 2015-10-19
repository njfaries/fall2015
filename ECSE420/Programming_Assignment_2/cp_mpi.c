#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "math.h"

//each process takes rows (size * i) + rank

int rank, size, numrows;


double ** read_user_matrix_from_file(char* filename, int* rows, int* columns)
{
	FILE *file;
	file = fopen(filename, "r");
}


int main(int argc, char * argv[])
{
	if (argv != 2) {printf("Please provide a matrix");}

	int ierr = MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); //sets rank
	MPI_Comm_size(MPI_COMM_WORLD, &size); //gets number of processes

	if (rank == 0) {
		get_number_of_rows(argv[1], &rows);
	}
	ierr = MPI_Finalize();
}