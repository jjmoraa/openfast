.PHONY: all build cart polar curl post

FASTFARM = ../build-single-debug/glue-codes/fast-farm/FAST.Farm

all: build cart polar curl post

build:
	$(MAKE) -f Makefile_OpenFAST compile

cart:
	cd task1_uniform_aligned && $(FASTFARM) input_cart_new.fstf

polar:
	cd task1_uniform_aligned && $(FASTFARM) input_polar_new.fstf

curl:
	cd task1_uniform_aligned && $(FASTFARM) input_curl_new.fstf

post:
	python task1.py
