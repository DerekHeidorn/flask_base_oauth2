import time
from sqlalchemy import Column, Integer, ForeignKey

from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from project.app.models.baseModel import BaseModel


class OAuth2Client(BaseModel, OAuth2ClientMixin):
    __tablename__ = 'tb_oauth2_client'  # oauth2_client'

    id = Column("oauth2cl_id", Integer, primary_key=True)

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


class OAuth2AuthorizationCode(BaseModel, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'tb_oauth2_code'  # 'oauth2_code'

    id = Column("oauth2cd_id", Integer, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey('tb_user.user_id', ondelete='CASCADE'))

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))


class OAuth2Token(BaseModel, OAuth2TokenMixin):
    __tablename__ = 'tb_oauth2_token'  # 'oauth2_token'

    id = Column("oauth2tkn_id", Integer, primary_key=True)

    user_id = Column("user_id", Integer, ForeignKey('tb_user.user_id', ondelete='CASCADE'))

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))
