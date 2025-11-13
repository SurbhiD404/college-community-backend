from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from django.conf import settings
import jwt

User = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware:
    
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner

    async def __call__(self, receive, send):
        
        self.scope['user'] = AnonymousUser()
        query_string = self.scope.get('query_string', b'').decode()
        qs = parse_qs(query_string)
        token_list = qs.get('token', None)
        if token_list:
            token = token_list[0]
            try:
                validated_token = UntypedToken(token)
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get('user_id')
                if user_id:
                    self.scope['user'] = await get_user(user_id)
            except Exception:
                self.scope['user'] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)
