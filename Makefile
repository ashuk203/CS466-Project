needle: NeedlemanWunsch.o
	clang++ NeedlemanWunsch.o -o $@

NeedlemanWunsch.o:
	clang++ -c NeedlemanWunsch.cpp NeedlemanWunsch.h

clean:
	rm -f *.o *.exe
