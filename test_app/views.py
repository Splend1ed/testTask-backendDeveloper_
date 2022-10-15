from pybase64 import b64encode, b64decode
from rest_framework import mixins, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from test_app.models import Url
from test_app.permissions import IsAdminUserOrAuthenticated
from test_app.serializers import UrlListSerializer, UrlSerializer


@api_view(["POST"])
@permission_classes((IsAdminUserOrAuthenticated,))
@authentication_classes((JWTAuthentication,))
def create_short_url(request):

    url = request.POST["default_url"]
    url_obj = Url.objects.create(default_url=url, user_id=request.user.id)
    encoded_id = b64encode(bytes(str(url_obj.id), "utf-8"), b"AK")
    short_url = f"http://{request.get_host()}/r/{encoded_id.decode('utf-8')}/"
    url_obj.short_url = short_url

    data = {
        "default_url": url_obj.default_url,
        "short_url": url_obj.short_url,
        "user_id": url_obj.user_id,
    }
    serializer = UrlSerializer(url_obj, data=data)

    if serializer.is_valid():
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((AllowAny,))
def redirect_to_url(request, enc_url):
    url_id = b64decode(bytes(enc_url, "utf-8"), b"AK").decode("utf-8")
    redirect_obj = Url.objects.get(id=url_id)
    redirect_obj.views += 1
    redirect_obj.save()

    return redirect(redirect_obj.default_url)


class UrlListView(ListAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlListSerializer
    permission_classes = (IsAdminUserOrAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Url.objects.all()
        return Url.objects.filter(user_id=self.request.user.id).all()


class UrlDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = (IsAdminUserOrAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Url.objects.all()
        return Url.objects.filter(user_id=self.request.user.id).all()
