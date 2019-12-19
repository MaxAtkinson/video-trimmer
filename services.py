import os
import uuid
import urllib.request

import models
import exceptions
from api import Session

import boto3
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


class TrimVideoProcessor:
    BUCKET_UPLOAD_NAME = 'hopster'
    URL_TEMPLATE = 'http://85072-c.ooyala.com/{}/DOcJ-FxaFrRg4gtDEwOjIwbTowODE7WK'  # noqa

    def __init__(self, video):
        self.video_id = video
        self.s3_client = boto3.client('s3')

    def generate_filename(self):
        return f'videos/{uuid.uuid4()}.mp4'

    def remove_temp_file(self, filename):
        print(f'Removing {filename}...')
        os.remove(filename)

    def download(self):
        print('Downloading Video...')
        path = self.generate_filename()
        urllib.request.urlretrieve(self.url, path)
        return path

    def process(self, src_path, t_start, t_end):
        print('Processsing...')
        duration = VideoFileClip(src_path).duration
        if t_start < 0 or t_start > t_end or t_end > duration:
            raise exceptions.InvalidLengthException('Invalid t_start or t_end')
        dest_path = self.generate_filename()
        ffmpeg_extract_subclip(src_path, t_start, t_end, targetname=dest_path)
        self.remove_temp_file(src_path)
        return dest_path

    def upload(self, dest_path):
        print('Uploading...')
        self.s3_client.upload_file(dest_path,
                                   self.BUCKET_UPLOAD_NAME,
                                   dest_path)
        self.remove_temp_file(dest_path)
        return f'https://{self.BUCKET_UPLOAD_NAME}.s3.eu-west-2.amazonaws.com/{dest_path}'  # noqa

    def run(self):
        print('Running...')
        try:
            downloaded_path = self.download()
            processed_path = self.process(downloaded_path,
                                          self.video.t_start,
                                          self.video.t_end)
            complete_path = self.upload(processed_path)
            self.complete(complete_path)
        except Exception as ex:
            self.error(ex)
        finally:
            print('Finished')
            self.db.commit()
            self.db.close()

    def complete(self, complete_path):
        print('Completed...')
        self.video.state = models.VIDEO_STATE_COMPLETED
        self.video.state_context = 'Uploaded successfully.'
        self.video.dest_url = complete_path

    def error(self, ex):
        print('Errored...')
        print(ex)
        self.video.state = models.VIDEO_STATE_ERROR
        self.video.state_context = str(ex)

    def __call__(self):
        print('Starting...')
        self.db = Session()
        self.video = self.db.query(models.Video).get(self.video_id)
        self.url = self.URL_TEMPLATE.format(self.video.src_url)
        self.run()
