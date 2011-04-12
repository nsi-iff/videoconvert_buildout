#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from xmlrpclib import Server
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call
from multiprocessing import Process
from time import sleep
from json import loads
from restfulie import Restfulie

FOLDER_PATH = abspath(dirname(__file__))

class VideoConvertTest(unittest.TestCase):

    def setUp(self):
        self.video_service = Restfulie.at("http://localhost:8080/").auth('test', 'test').as_('application/json')
        self.sam = Restfulie.at('http://localhost:8888/').auth('test', 'test').as_('application/json')
        self.uid_list = []

    def testConvertion(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)
	response = self.video_service.post(video=b64_encoded_video)
	print response.body, ' oi'
	uid = response.resource().key
        self.uid_list.append(uid)
        self.assertTrue(isinstance(uid,unicode))

        self.assertFalse(self.video_service.get(key=uid).resource().done)

        sleep(60)

        self.assertTrue(self.video_service.get(key=uid).resource().done)
        video = loads(self.sam.get(key=uid).body)

        self.assertTrue(isinstance(video, dict))
        self.assertEquals(len(video), 4)

        video_data = decodestring(video.get('data'))
        self.assertTrue(video_data)

if __name__ == '__main__':
        rabbitmq_ctl = join(FOLDER_PATH, '..', 'bin', 'rabbitmqctl')
        rabbitmq_server = join(FOLDER_PATH, '..', 'bin', 'rabbitmq-server')
        videoconvert_ctl = join(FOLDER_PATH, '..', 'bin', 'videoconvert_ctl')
        worker = join(FOLDER_PATH, '..', 'bin', 'start_worker -name test_worker')
        stop_worker = join(FOLDER_PATH, '..', 'bin', 'stop_worker')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        try:
            call("%s -detached" % rabbitmq_server, shell=True)
            call("%s start" % videoconvert_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            call("%s" % worker, shell=True)
            sleep(5)
            unittest.main()
        finally:
            sleep(1)
            call("%s stop" % rabbitmq_ctl, shell=True)
            call("%s stop" % videoconvert_ctl, shell=True)
            call("%s test_worker " % stop_worker, shell=True) 
            call("%s test" % del_user, shell=True)

