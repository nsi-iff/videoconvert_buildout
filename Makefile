PYTHON=python
PIP=pip

all: clean celery gstreamer rest_mq redisapi buildout nsivideoconvert test
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

celery:
	${PIP} install celery

nsivideoconvert:
	@rm -Rf nsi.videoconvert-0.1
	@rm -rf nsi.sam-0.1.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.videoconvert-0.1.tar.gz
	tar -vzxf nsi.videoconvert-0.1.tar.gz
	cd nsi.videoconvert-0.1 && ${PYTHON} setup.py install
	@rm -Rf nsi.videoconvert-0.1
	@rm -rf nsi.videoconvert-0.1.tar.gz

nsimultimedia:
	@rm -Rf nsi.multimedia-0.1.2
	@rm -rf nsi.multimedia-0.1.2.tar.gz
	wget http://newton.iff.edu.br/pypi/nsi.multimedia-0.1.2.tar.gz
	tar -vzxf nsi.multimedia-0.1.2.tar.gz
	cd nsi.multimedia-0.1.2 && ${PYTHON} setup.py install
	@rm -Rf nsi.multimedia-0.1.2
	@rm -rf nsi.multimedia-0.1.2.tar.gz

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

