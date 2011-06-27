#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import sys
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call, Popen
from multiprocessing import Process
from time import sleep
from datetime import datetime
from functools import wraps
from json import loads
from restfulie import Restfulie

FOLDER_PATH = abspath(dirname(__file__))

def time_it(function_name):
    def inner_timer(function):
        def wrapped(*args, **kwargs):
            start = datetime.now()
            result = function(*args, **kwargs)
            end = datetime.now()
            execution_time = end - start
            print "%s took %d seconds and %d microseconds." % (function_name, execution_time.seconds, execution_time.microseconds)
            return result
        return wrapped
    return inner_timer

class PerformanceTest(object):

    def __init__(self, threads, videos, videos_size):
        self.threads = int(threads)
        self.videos = int(videos)
        self.videos_size = int(videos_size)

    def start(self):
        self.video_list = []
        self.uid_list = []

        self.base_video = self._read_input_file()
        self.video_list = self._make_video_list()
        self.uid_list = self._post_videos()

    @time_it('Read input file')
    def _read_input_file(self):
        video = open(join(FOLDER_PATH, 'input', 'rubik.flv')).read()
        return video

    @time_it('Make the video list')
    def _make_video_list(self):
        return [b64encode(self.base_video * self.videos_size) for i in range(self.videos)]

    @time_it('Send all videos to the web server')
    def _post_videos(self):
        video_convert= Restfulie.at('http://localhost:8885').auth('test', 'test').as_('application/json')
        return [video_convert.post(video=video) for video in self.video_list]

def parse_args():
    args_number = len(sys.argv) - 1
    args = sys.argv[1:]

    if not args_number == 3:
        print "Número de argumentos inválidos."
        print_help()
        exit(1)
    else:
        return {"threads":args[0], "videos":args[1], "videos_size":args[2]}

def print_help():
    print("Devem ser passados três argumentos.\n")
    print("O primeiro representa quantos processos serão usados.\n")
    print("O segundo representa a quantidade de vídeos que serão enviados ao servidor\n")
    print("O terceiro representa o tamanho dos vídeos enviados ao servidor.\n")

if __name__ == '__main__':
    print "Necessario que o SAM esteja rodando na porta padrao com o usuario\n" + \
          "'test' e senha 'test' criados."
    videogranulate_ctl = join(FOLDER_PATH, '..', 'bin', 'videogranulate_ctl')
    add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
    del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
    try:
        call("%s start" % videogranulate_ctl, shell=True)
        call("%s test test" % add_user, shell=True)
        args = parse_args()
        PerformanceTest(**args).start()
    finally:
        call("%s stop" % videogranulate_ctl, shell=True)
        call("%s test" % del_user, shell=True)

