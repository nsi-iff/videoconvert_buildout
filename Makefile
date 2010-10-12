PYTHON=python

all: clean gstreamer rest_mq redisapi buildout test
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

redisapi:
	@rm -Rf txredisapi
	git clone git://github.com/fiorix/txredisapi.git
	cd txredisapi && $(PYTHON) setup.py install
	@rm -Rf txredisapi

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoConverting.py

rest_mq:
	@rm -rf restmq restmq.tar.gz
	git clone git://github.com/gleicon/restmq.git
	@rm -rf restmq.tar.gz

