from concurrent.futures import ThreadPoolExecutor

from flask import abort, jsonify
from flask_restful import Resource, reqparse

import models
import settings
from api import Session
from services import TrimVideoProcessor

parser = reqparse.RequestParser()
parser.add_argument('t_start')
parser.add_argument('t_end')
parser.add_argument('src_url')
executor = ThreadPoolExecutor(settings.THREAD_WORKERS)
db = Session()


class VideoResource(Resource):
    def get(self, video_id):
        video = db.query(models.Video).get(video_id)
        if not video:
            return abort(404)
        return jsonify(video.as_dict)

    def delete(self, video_id):
        db.query(models.Video).filter_by(id=video_id).delete()
        db.commit()
        return jsonify({'deleted': True})

    def put(self, video_id):
        video = db.query(models.Video).get(video_id)
        if not video:
            return abort(404)

        args = parser.parse_args()

        for key, val in args:
            setattr(video, key, val)

        db.commit()
        return video.as_dict


class VideoListResource(Resource):
    def get(self):
        videos = db.query(models.Video).all()
        return jsonify([video.as_dict for video in videos])

    def post(self):
        # k3YmNzaTE6XAeocyVuctpmcXe4g_iNWh
        args = parser.parse_args()
        video = models.Video(**args)
        db.add(video)
        db.commit()
        executor.submit(TrimVideoProcessor(video.id))
        db.close()
        return video.as_dict


def configure(api):
    api.add_resource(VideoListResource, '/videos')
    api.add_resource(VideoResource, '/videos/<video_id>')
