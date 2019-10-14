from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import authentication, permissions, status
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .oauth2provider import Oauth2Provider

from .models import User
from .backends import EmailAuthBackend
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

import json


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login_test(request):
    serialized = LoginSerializer(data=request.data)
    print('before')
    if serialized.is_valid():
        print('valid')
        print(serialized.data['email'])
        print(serialized.data['password'])
        user = EmailAuthBackend.authenticate(username=serialized.data['email'], password=serialized.data['password'])
        print(user)
        if user is not None :
            print('not none')
            auth.login(request, user)
            return Response(request.user, status=status.HTTP_200_OK)
        else:
            print("noneee--")
            return Response(serialized._errors, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def social_login(request):
    access_token = request.data.get("access_token")
    provider = request.data.get("provider")
    api_info = Oauth2Provider(provider, access_token).get_user_details()
    if api_info.status_code == 200:
        result = json.loads(api_info.text)
        try:
            user = User.objects.get(email = result['email'])
        except User.DoesNotExist:
            pass
        try:
            user = User.objects.create(email = result['email'])
        except IntegrityError:
            user.password = user.set_unusable_password()

        token,_ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                    status=HTTP_200_OK)
    else:
        return Response(status=HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = EmailAuthBackend.authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token,_ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


#curl -i -H "Authorization: Token 2536ac6c9e00c5c4ace98395186cd1e42126adf4" -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://localhost:8000/test/

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def test(request):
    return Response({'email': request.user.email},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def logout(request):
    request.user.auth_token.delete()
    return Response({'msg': 'Successfully logged out!'},status=status.HTTP_200_OK)



