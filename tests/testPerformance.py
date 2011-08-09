#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import sys
from threading import Thread
from subprocess import call
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from datetime import datetime
from restfulie import Restfulie

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

class PerformanceTest(object):

    def __init__(self, threads, videos, videos_size):
        self.threads = int(threads)
        self.videos = int(videos)
        self.videos_size = int(videos_size)
        self.videos_over_threads = self.videos/self.threads
        self.video_list_per_thread = []

    def start(self):
        self.video_list = []
        self.uid_list = []

        print "Sending %d videos with %d parts of 1,5mb each, using up to %d threads" % (self.videos, self.videos_size, self.threads)
        self.base_video = self._read_input_file()
        self.video_list = self._make_video_list()
        self.video_list_per_thread = self._split_video_lists()
        self._start_thread_post_videos()

    @time_it('Delete all temporary videos')
    def remove_videos(self):
        for uid in self.uid_list:
            Restfulie.at('http://localhost:8888').auth('test', 'test').as_('application/json').delete(key=uid)

    @time_it('Read input file')
    def _read_input_file(self):
        video = open(join(FOLDER_PATH, 'input', 'rubik.flv')).read()
        return video

    @time_it('Distributing the videos into equal lists')
    def _split_video_lists(self):
        temp_video_list = []
        splitted_video_list = []
        for (index, video) in enumerate(self.video_list, start=1):
            if index % self.videos_over_threads == 0:
                temp_video_list.append(video)
                splitted_video_list.append(temp_video_list)
                temp_video_list = []
            else:
                temp_video_list.append(video)
        return splitted_video_list

    @time_it('Make the video list')
    def _make_video_list(self):
        return [b64encode(self.base_video * self.videos_size) for i in range(self.videos)]

    @time_it('Start all the threads to post videos')
    def _start_thread_post_videos(self):
        self.threads = []

        @time_it('A thread to post videos')
        def post_videos(video_list):
            video_convert = Restfulie.at('http://localhost:8080').auth('test', 'test').as_('application/json')
            uids = [video_convert.post(video=video).resource().key for video in video_list]
            self.uid_list.extend(uids)

        for video_list in self.video_list_per_thread:
            thread = Thread(target=post_videos, args=(video_list,))
            self.threads.append(thread)

        for thread in self.threads:
            thread.start()

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
    print("O terceiro representa o tamanho dos vídeos (em megabytes) que serão enviados ao servidor.\n")

if __name__ == '__main__':
    print "Necessario que o SAM esteja rodando na porta padrao com o usuario\n" + \
          "'test' e senha 'test' criados."
    videoconvert_ctl = join(FOLDER_PATH, '..', 'bin', 'videoconvert_ctl')
    add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
    del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
    args = parse_args()
    videos_uid = []
    try:
        call("%s start" % videoconvert_ctl, shell=True)
        call("%s test test" % add_user, shell=True)
        test = PerformanceTest(**args)
        test.start()
    finally:
        for thread in test.threads:
            thread_uids = thread.join()
        test.remove_videos()
        call("%s stop" % videoconvert_ctl, shell=True)
        call("%s test" % del_user, shell=True)

