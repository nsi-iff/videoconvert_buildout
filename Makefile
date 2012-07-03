PYTHON=python
PIP=pip

all: clean pip gstreamer argparse redisapi buildout nsivideoconvert nsimultimedia restfulie should_dsl cyclone funkload test
clean:
	rm -Rf .installed.cfg bin downloads run develop-eggs eggs log parts

pip:
	easy_install pip

restfulie:
	$(PIP) install restfulie

cyclone:
	pip install twisted cyclone

nsivideoconvert:
	pip install https://github.com/nsi-iff/nsi.videoconvert/tarball/master

nsimultimedia:
	pip install https://github.com/nsi-iff/nsi.multimedia/tarball/master

should_dsl:
	pip install should-dsl

redisapi:
	@rm -Rf txredisapi
	git clone git://github.com/fiorix/txredisapi.git
	cd txredisapi && $(PYTHON) setup.py install
	@rm -Rf txredisapi

funkload:
	sudo apt-get install python-dev python-setuptools python-webunit python-docutils gnuplot -y
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

argparse:
	sudo apt-get install python-argparse -y

gstreamer:
	sudo apt-get install python-gst0.10 gstreamer-tools gstreamer0.10-ffmpeg gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-good gstreamer0.10-x python-gtk2 -y

buildout:
	$(PYTHON) bootstrap.py
	bin/buildout -vv

test:
	cd tests && $(PYTHON) testVideoConverting.py
