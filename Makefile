.PHONY: all install

all:
	@echo "Nothing to do here. Run 'make install' as root."

install:
	cp odbcdump.py /usr/local/bin/odbcdump
	chmod 755 /usr/local/bin/odbcdump
