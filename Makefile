LD = clang++


#Type in 'make run-needle' into command prompt
run-needle: need-wunsch
	./need-wunsch
	make clean

run-hirschberg: hberg
	./hberg
	make clean


#Other rules (can ignore)...
need-wunsch: NeedlemanWunsch.o
	$(LD) NeedlemanWunsch.o -o $@

hberg: Hirschberg.o
	$(LD) Hirschberg.o -o $@

NeedlemanWunsch.o:
	$(LD) -c */NeedlemanWunsch.cpp */NeedlemanWunsch.h

Hirschberg.o:
	$(LD) -c */Hirschberg.cpp */Hirschberg.h


clean:
	rm -f *.o
