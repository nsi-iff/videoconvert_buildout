import unittest
from os.path import dirname, abspath, join
from json import dumps, loads
from base64 import b64encode
from restfulie import Restfulie
from funkload.FunkLoadTestCase import FunkLoadTestCase
from funkload.Lipsum import Lipsum
from funkload.utils import Data


FOLDER_PATH = abspath(dirname(__file__))


class VideoConvertBench(FunkLoadTestCase):
    """This test use a configuration file Simple.conf."""

    def __init__(self, *args, **kwargs):
        FunkLoadTestCase.__init__(self, *args, **kwargs)
        """Setting up the benchmark cycle."""
        self.server_url = self.conf_get('main', 'url')
        self.sam = Restfulie.at('http://localhost:8888/').auth('test', 'test').as_('application/json')
        self.lipsum = Lipsum()
        self.uid_list = []
        self.video_file = b64encode(open(join(FOLDER_PATH, 'input', 'rubik.flv')).read())

    def test_convert(self):
        server_url = self.server_url
        self.setBasicAuth('test', 'test')

        # The description should be set in the configuration file

        body = dumps({'video': self.video_file})

        # begin of test ---------------------------------------------
        self.post(server_url, description='Send many videos with 5mb each.',
                  params=Data('application/json', body))
        response = loads(self.getBody())
        self.uid_list.extend(response.values())
        # end of test -----------------------------------------------

    def tearDown(self):
        for uid in self.uid_list:
            self.sam.delete(key=uid)


if __name__ in  ('__main__', 'main'):
       unittest.main()
