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
        self.video_service = Restfulie.at("http://test:test@localhost:8080/").as_('application/json').accepts('application/json')
        self.sam = Restfulie.at('http://localhost:8888/').as_('application/json')
        self.uid_list = []

    def testConvertion(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)
        uid = self.video_service.post({'video':b64_encoded_video}).resource().key
        self.uid_list.append(uid)
        self.assertTrue(isinstance(uid,unicode))

        self.assertFalse(self.video_service.get({'key':uid}).resource().done)

        sleep(60)

        self.assertTrue(self.video_service.get({'key':uid}).resource().done)
        video = loads(self.sam.get({'key':uid}).body)
        self.assertTrue(isinstance(video, dict))
        self.assertEquals(len(video), 3)

        video_data = decodestring(video.get('data'))
        self.assertTrue(video_data)

if __name__ == '__main__':
        videoconvert_ctl = join(FOLDER_PATH, '..', 'bin', 'videoconvert_ctl')
        restmq_ctl = join(FOLDER_PATH, '..', 'bin', 'restmq_ctl')
        slave = join(FOLDER_PATH, '..', 'etc', 'slave.py')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        try:
            call("%s start" % restmq_ctl, shell=True)
            call("%s start" % videoconvert_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            slave_process = Process(target=call, args=(slave,), kwargs={"shell":True})
            slave_process.start()
            sleep(5)
            unittest.main()
        finally:
            slave_process.terminate()
            sleep(1)
            call("%s stop" % restmq_ctl, shell=True)
            call("%s stop" % videoconvert_ctl, shell=True)
            call("%s test" % del_user, shell=True)

