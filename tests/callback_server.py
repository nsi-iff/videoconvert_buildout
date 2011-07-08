import json
import cyclone.web
from twisted.internet import defer
from twisted.application import service, internet

class HttpHandler(cyclone.web.RequestHandler):

    def _load_request_body_as_json(self):
        return json.loads(self.request.body)

    def post(self):
        video = self._load_request_body_as_json()
        video_is_done = video.get('done')
        if video_is_done:
            video_status = "done"
            open('/tmp/done', 'w+').write('done')
        else:
            video_status = "not done"
            open('/tmp/not_done', 'w+').write('not done')
        self.write("Video with uid %s is %s." % (video.get('uid'), video_is_done))

class CallbackService(cyclone.web.Application):

    def __init__(self):
        handlers = [
            (r"/", HttpHandler),
        ]

        settings = {
                'xheaders':True,
                }

        cyclone.web.Application.__init__(self, handlers, **settings)

application = service.Application("Callback Service")
srv = internet.TCPServer(8887, CallbackService(), interface='0.0.0.0')
srv.setServiceParent(application)

