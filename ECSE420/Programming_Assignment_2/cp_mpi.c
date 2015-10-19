#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "math.h"


int main(int argc, char * argv[])
{
	int ierr = MPI_Init(&argc, &argv);
	printf("%d", ierr);
	ierr = MPI_Finalize();
}