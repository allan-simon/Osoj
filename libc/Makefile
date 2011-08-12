all: libs

libs: lib.c
	gcc -fPIC -shared -Wl,-soname,libopenojlibc.so.1 -o libopenojlibc.so.1.0 lib.c
	ln -sf libopenojlibc.so.1.0 libopenojlibc.so.1
	ln -sf libopenojlibc.so.1	libopenojlibc.so

clean:
	rm -f libopenojlibc.so.1.0 libopenojlibc.so.1 libopenojlibc.so lib.o
