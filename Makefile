LD = clang++
EXENAME = need-wunsch hberg
OBJS: Hirschberg.o NeedlemanWunsch.o

.PHONY: need-wunsch hberg $(OBJS)

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
