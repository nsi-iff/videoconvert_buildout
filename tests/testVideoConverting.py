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
from should_dsl import *

FOLDER_PATH = abspath(dirname(__file__))

class VideoConvertTest(unittest.TestCase):

    def setUp(self):
        self.video_service = Restfulie.at("http://localhost:8884/").auth('test', 'test').as_('application/json')
        self.sam = Restfulie.at('http://localhost:8888/').auth('test', 'test').as_('application/json')
        self.uid_list = []

    def testDirectConvertion(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)
        uid = self.video_service.post(video=b64_encoded_video, callback='http://localhost:8887/').resource().key
        self.uid_list.append(uid)

        uid |should| be_instance_of(unicode)

        self.video_service.get(key=uid).resource() |should_not| be_done

        sleep(60)

        self.video_service.get(key=uid).resource() |should| be_done
        video = loads(self.sam.get(key=uid).body)
        video.keys() |should| have(4).items
        video_data = decodestring(video.get('data').get('video'))
        video_data |should_not| have(0).characters

    def testConvertionFromSam(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)

        response = self.sam.put(value={"video":b64_encoded_video, "converted":False})
        response.code |should| equal_to('200')
        video_key = response.resource().key
        self.uid_list.append(video_key)

        self.video_service.post(video_uid=video_key, filename='teste.flv')
        self.video_service.get(key=video_key).resource() |should_not| be_done

        sleep(60)

        self.video_service.get(key=video_key).resource() |should| be_done
        video = loads(self.sam.get(key=video_key).body)
        video.keys() |should| have(4).items
        video_data = decodestring(video.get('data').get('video'))
        video_data |should_not| have(0).characters

    def testDownloadConvertion(self):

        uid_video_download = self.video_service.post(video_link='http://localhost:8887/rubik.flv', callback='http://localhost:8887').resource().key
        self.uid_list.append(uid_video_download)

        sleep(60)

        convertion = self.video_service.get(key=uid_video_download).resource()

        convertion |should| be_done

    def tearDown(self):

        for uid in self.uid_list:
            self.sam.delete(key=uid)

if __name__ == '__main__':
        videoconvert_ctl = join(FOLDER_PATH, '..', 'bin', 'videoconvert_ctl')
        worker = join(FOLDER_PATH, '..', 'bin', 'start_worker -name test_worker')
        stop_worker = join(FOLDER_PATH, '..', 'bin', 'stop_worker')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        callback_server = join(FOLDER_PATH, "callback_server.py")
        try:
            call("twistd -y %s" % callback_server, shell=True)
            call("%s start" % videoconvert_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            call("%s" % worker, shell=True)
            sleep(5)
            unittest.main()
        finally:
            sleep(1)
            call("kill -9 `cat twistd.pid`", shell=True)
            call("%s stop" % videoconvert_ctl, shell=True)
            call("%s test_worker " % stop_worker, shell=True)
            call("%s test" % del_user, shell=True)

