#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from datetime import datetime
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call, Popen
from multiprocessing import Process
from time import sleep
from json import loads
from restfulie import Restfulie
from should_dsl import *

FOLDER_PATH = abspath(dirname(__file__))

class time_it(object):

    def __init__(self, function_name):
        self.function_name = function_name

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            start = datetime.now()
            result = function(*args, **kwargs)
            end = datetime.now()
            execution_time = end - start
            print "%s took %d seconds and %d microseconds." % (self.function_name, execution_time.seconds, execution_time.microseconds)
            return result
        return wrapper

class VideoConvertTest(unittest.TestCase):

    def setUp(self):
        self.video_convert_service = Restfulie.at("http://localhost:8884/").auth('test', 'test').as_('application/json')
        self.sam = Restfulie.at("http://localhost:8888/").auth('test', 'test').as_('application/json')
        self.uid_list = []

        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        self.b64_encoded_video = b64encode(input_video)
        response = self.video_convert_service.post(video=self.b64_encoded_video, filename='video1.flv', callback='http://localhost:8887/').resource()
        self.video_key = response.key
        self.uid_list.append(self.video_key)

    @time_it('Convertion of a video.')
    def testConvert(self):
        while not self.video_convert_service.get(key=self.video_key).resource().done:
            sleep(1)

    def tearDown(self):
        for uid in self.uid_list:
            self.sam.delete(key=uid)

if __name__ == '__main__':
        print "Necessario que o SAM esteja rodando na porta padrao com o usuario\n" + \
          "'test' e senha 'test' criados."
        videoconvert_ctl = join(FOLDER_PATH, '..', 'bin', 'videoconvert_ctl')
        worker = join(FOLDER_PATH, '..', 'bin', 'start_worker -name test_worker > /dev/null 2> /dev/null')
        stop_worker = join(FOLDER_PATH, '..', 'bin', 'stop_worker test_worker')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        callback_server = join(FOLDER_PATH, "callback_server.py")
        try:
            call("twistd -y %s" % callback_server, shell=True)
            call("%s start" % videoconvert_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            call("%s" % worker, shell=True)
            unittest.main()
        finally:
            call("kill -9 `cat twistd.pid`", shell=True)
            call("%s" % stop_worker, shell=True)
            call("%s stop" % videoconvert_ctl, shell=True)
            call("%s test" % del_user, shell=True)



