#include <stdio.h>
#include <stdlib.h>
// #include <mpi.h>
#include "math.h"

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


void enter_line_into_matrix(char * line)
{
	int i;
	char *ptr;
	double value;
	value = strtod(line, &line);
	printf("Rest of the line: %s", line);
	printf("Value: %lf\n", value);

}

int main(int argc, char * argv[])
{
	FILE *file;
	file = fopen(argv[1], "r");
	char * line;
	size_t size = 0;
	advance_number_of_rows(file, 2);
	getline(&line, &size, file);
	printf("Line read: %s\n", line);
	printf("Size: %zu\n", size);
	enter_line_into_matrix(line);
}