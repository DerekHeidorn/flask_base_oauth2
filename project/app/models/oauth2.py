import time
from sqlalchemy import Column, Integer, ForeignKey

from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from project.app.models.baseModel import BaseModel


class OAuth2Client(BaseModel, OAuth2ClientMixin):
    __tablename__ = 'TB_OAUTH2_CLIENT'  #oauth2_client'

    id = Column("OAUTH2CL_ID", Integer, primary_key=True)


class OAuth2AuthorizationCode(BaseModel, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'TB_OAUTH2_CODE' # 'oauth2_code'

    id = Column("OAUTH2CD_ID", Integer, primary_key=True)

    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.USER_ID', ondelete='CASCADE'))


class OAuth2Token(BaseModel, OAuth2TokenMixin):
    __tablename__ = 'TB_OAUTH2_TOKEN' # 'oauth2_token'

    id = Column("OAUTH2TKN_ID", Integer, primary_key=True)

    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.USER_ID', ondelete='CASCADE'))

    def is_refresh_token_expired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()