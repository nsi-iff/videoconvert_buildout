#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from xmlrpclib import Server
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call
from multiprocessing import Process
from time import sleep

FOLDER_PATH = abspath(dirname(__file__))

class VideoConvertTest(unittest.TestCase):

    def setUp(self):
        self.video_service = Server("http://test:test@localhost:8080/xmlrpc")
        self.sam = Server("http://video:convert@localhost:8888/xmlrpc")
        self.uid_list = []

    def testConvertion(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)
        uid = self.video_service.convert(b64_encoded_video)
        self.uid_list.append(uid)
        self.assertTrue(isinstance(uid,str))

        sleep(50)

        self.assertTrue(self.video_service.done(uid))
        video_dict = eval(self.sam.get(uid))
        self.assertTrue(isinstance(video_dict, dict))
        self.assertEquals(len(video_dict), 4)

        video_data = decodestring(video_dict.get('data'))
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

