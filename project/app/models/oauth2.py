import time
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, DateTime, Table
from sqlalchemy.orm import relationship, base

from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)

from project.app.models.baseModel import BaseModel

class OAuth2Client(BaseModel, OAuth2ClientMixin):
    __tablename__ = 'TB_OAUTH2_CLIENT'  #oauth2_client'

    id = Column("OAUTH2CL_ID", Integer, primary_key=True)
    user_id = Column("USER_ID", Integer, ForeignKey('user.id', ondelete='CASCADE'))
    #user = relationship('User')
    
    def check_response_type(self, response_type):
        grant_maps = {'code': 'authorization_code', 'token': 'implicit'}
        grant_type = grant_maps.get(response_type)
        if not grant_type:
            return False
        return self.check_grant_type(grant_type)

    def check_grant_type(self, grant_type):
        return grant_type in self.allowed_grants.split()

class OAuth2AuthorizationCode(BaseModel, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'TB_OAUTH2_CODE' # 'oauth2_code'

    id = Column("OAUTH2CD_ID", Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    #user = relationship('User')


class OAuth2Token(BaseModel, OAuth2TokenMixin):
    __tablename__ = 'TB_OAUTH2_TOKEN' # 'oauth2_token'

    id = Column("OAUTH2TKN_ID", Integer, primary_key=True)
    user_id = Column("USER_ID", Integer, ForeignKey('TB_USER.USER_ID', ondelete='CASCADE'))
    #user = relationship('User')

    def isRefreshTokenExpired(self):
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at < time.time()