import json
import cyclone.web
from twisted.application import service, internet

class HttpHandler(cyclone.web.RequestHandler):

    def _load_request_body_as_json(self):
        return json.loads(self.request.body)

    def post(self):
        video = self._load_request_body_as_json()
        video_is_done = video.get('done')
        if video_is_done:
            video_status = "done"
        else:
            video_status = "not done"
        self.write("Video with uid %s is %s." % (video.get('uid'), video_is_done))

class FileHandler(cyclone.web.RequestHandler):

    def get(self):
        video =  open('input/rubik.flv', 'r')
        video_data = video.read()
        video.close()

        self.write(video_data)
        self.finish()


class CallbackService(cyclone.web.Application):

    def __init__(self):
        handlers = [
            (r"/", HttpHandler),
            (r"/rubik.flv", FileHandler),
        ]

        settings = {
                'xheaders':True,
                }

        cyclone.web.Application.__init__(self, handlers, **settings)

application = service.Application("Callback Service")
srv = internet.TCPServer(8887, CallbackService(), interface='0.0.0.0')
srv.setServiceParent(application)

