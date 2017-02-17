from django.test import TestCase
import simplejson as json


class VideoTest(object):
    videos_api_url = '/api/videos/'
    specific_video_url = "%s%s/"

    def get_video_list(self):
        return self.client.get(self.videos_api_url)

    def create_video(self, video):
        return self.client.post(self.videos_api_url, video)

    def delete_video(self, video_id):
        return self.client.delete(self.specific_video_url % (self.videos_api_url, video_id))

    def update_video(self, video_id, video):
        return self.client.put(self.specific_video_url % (self.videos_api_url, video_id), video,
                               content_type='application/json')

    def get_video(self, video_id):
        return self.client.get(self.specific_video_url % (self.videos_api_url, video_id))


class VideoViewsTestCase(TestCase, VideoTest):
    def __init__(self, *args, **kwargs):
        super(VideoViewsTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        pass

    def test_videos_endpoint(self):
        video = dict(name='Testvideo',
                     url="https://www.youtube.com/embed/93FprsmspCs")

        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 201)

        resp = self.get_video_list()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_create_video_bad_url(self):
        video = dict(name='Testvideo',
                     url='test.html')
        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {"url": ["Enter a valid URL."]})

    def test_create_video_embeded_url(self):
        video = dict(name='Testvideo',
                     url="https://www.youtube.com/embed/93FprsmspCs")
        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json().get('url'), "https://www.youtube.com/embed/93FprsmspCs?rel=0&autoplay=1")

    def test_create_video_watch_url(self):
        video = dict(name='Testvideo',
                     url="https://www.youtube.com/watch?v=hfjHJneVonE")
        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json().get('url'), "https://www.youtube.com/embed/hfjHJneVonE?rel=0&autoplay=1")

    def test_create_video_non_youtube_url(self):
        video = dict(name='Testvideo',
                     url='https://www.dominos.com/en/pages/order/confirmation.jsp')
        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), [u"[u'Not a valid YouTube link.']"])

    def test_delete_video(self):
        video = dict(name='Testvideo',
                     url="https://www.youtube.com/embed/93FprsmspCs")
        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 201)
        resp = self.delete_video(resp.json().get('id'))
        self.assertEqual(resp.status_code, 200)

    def test_cannot_update_to_bad_url(self):
        video = dict(name='Testvideo',
                     url="https://www.youtube.com/embed/93FprsmspCs")
        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json().get('url'), "https://www.youtube.com/embed/93FprsmspCs?rel=0&autoplay=1")
        video = resp.json()
        video['url'] = 'kekeke'
        resp = self.update_video(video.get('id'), json.dumps(video))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {u'url': [u'Enter a valid URL.']})

    def test_can_update_to_good_url(self):
        video = dict(name='Testvideo',
                     url="https://www.youtube.com/embed/93FprsmspCs")

        resp = self.create_video(video)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json().get('url'), "https://www.youtube.com/embed/93FprsmspCs?rel=0&autoplay=1")
        video = resp.json()
        video['url'] = 'https://www.youtube.com/watch?v=hfjHJneVonE'
        resp = self.update_video(video.get('id'), json.dumps(video))
        self.assertEqual(resp.status_code, 200)
