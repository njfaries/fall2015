#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <mpi.h>
#include <sys/time.h>

#define dim 888


int main(int argc, char **argv){

	int rank,size,i,j,k,local_N; 
	double l;
	struct timeval start, end; // struct used to compute execution time

	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Status status;	

	if (rank==0) {
	
		allocate_matrix_A();
		initialize_matrix_A();

	}

	local_N = N / size;

	double** local_A;
	allocate_matrix_local_A();


	for (all rows N) {

		if ( not part that P0 will get) {

			if (rank == 0) // should send the rows
				MPI_Send(A[i], ....); 
				// to whom is should send it??? --> i/local_N
			else {
				if (is the owner of local row)
					MPI_Recv(local_A[i%(local_N)], ...);
					// where i should put it?? --> i%local_N
			}
		}
		else { // part that P0 will keep
			if (rank == 0) {
				for (j=0; j<dim; j++) 
					local_A[i%(local_N)][j] = A[i][j];
			}
		}
	}



	for (k = 0; k < dim-1; k++) {  // k-iteration of GE
		
		// allocate buffer
		double* buffer;
		buffer = (double*) malloc((dim-k)*sizeof(double));
	
		
		if (owner of pivot row) {  // should send the row
		
			// pack data @ buffer 
			for (j = k; j < dim; j++)
				buffer[j-k] = local_A[k%local_N][j];
			
			// collective or p2p
			MPI_Bcast(buffer, ...);

		}else { // should receive the row

			MPI_Bcast(buffer, ...);
		}


		// then execute the main GE kernel !!!!
		for (i=k+1; i<dim; i++) {
		
			if (rank == i/local_N) {

				l = local_A[i%local_N][k] / buffer[0];
				for (j=k+1; j<dim; j++)
					local_A[i%local_N][j] = local_A[i%local_N][j] - l*buffer[j-k];
			}
		}

		free(buffer);
	}


	// reverse the decomposition process
	for (all rows) {

		if (not part that P0 has) {
			
			if (rank != 0) // should sent the row back to P0

				MPI_Send(local_A[i%local_N], ...);

			else	// P0 should receive that 

				MPI_Recv(A[i], ...);
		}			
		else {  // part that P0 has

			if (rank == 0) { // just copy P0's local_A back to the main one
				for (j=0; j<dim; j++)
					A[i][j] = local_A[i%local_N][j];
			}
		}
	}


	MPI_Finalize();

return 0;
}

