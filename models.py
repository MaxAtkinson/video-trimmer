import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

from api import engine

Base = declarative_base()

VIDEO_STATE_IN_PROGRESS = 'IN PROGRESS'
VIDEO_STATE_ERROR = 'ERROR'
VIDEO_STATE_COMPLETED = 'COMPLETED'


class Video(Base):
    __tablename__ = 'videos'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    t_start = db.Column(
        db.Integer,
        nullable=False
    )
    t_end = db.Column(
        db.Integer,
        nullable=False
    )
    src_url = db.Column(
        db.String(250),
        nullable=False
    )
    dest_url = db.Column(
        db.String(120),
        nullable=True
    )
    state = db.Column(
        db.String(20),
        nullable=False,
        default=VIDEO_STATE_IN_PROGRESS
    )
    state_context = db.Column(
        db.String(100),
        nullable=True
    )

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'src_url': self.src_url,
            'dest_url': self.dest_url,
            'state': self.state,
            'state_context': self.state_context
        }

    def __repr__(self):
        return f'<Video {src_url}>'


Base.metadata.create_all(engine)
