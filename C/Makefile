#this is make file
CC=gcc
test: max.o mooc1.c
	$(CC) max.o mooc1.c -o test
max.o: max.c
	$(CC) -c max.c
.PHONY: clean
clean:
	#-rm test max.o
	-rm max.o
