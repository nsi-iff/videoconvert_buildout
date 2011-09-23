PYTHON=python
PIP=pip

all: clean pip gstreamer redisapi buildout nsivideoconvert nsimultimedia restfulie should_dsl cyclone funkload test
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

pip:
	easy_install pip

restfulie:
	$(PIP) install restfulie

cyclone:
	pip install twisted cyclone

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

should_dsl:
	pip install should-dsl

redisapi:
	@rm -Rf txredisapi
	git clone git://github.com/fiorix/txredisapi.git
	cd txredisapi && $(PYTHON) setup.py install
	@rm -Rf txredisapi

funkload:
	sudo apt-get install python-dev python-setuptools python-webunit python-docutils gnuplot
	pip install funkload

convert_test:
	cd tests && python testPerformanceVideoConvert.py

load_test:
	bin/videoconvert_ctl start
	bin/add-user.py test test
	cd tests && fl-run-bench testFunkLoad.py VideoConvertBench.test_convert
	cd tests && fl-build-report --html videoconvert-bench.xml -r funkload_report
	bin/videoconvert_ctl stop
	bin/del-user.py test

load_test_report:
	cd tests && fl-build-report --html videoconvert-bench.xml -r funkload_report

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools gstreamer0.10-ffmpeg gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-good gstreamer0.10-x python-gtk2

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoConverting.py
