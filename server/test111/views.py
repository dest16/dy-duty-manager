from rest_framework import viewsets
from .models import Avatar, Site, AccessKey, Profile, User, HolidaysAndFestivals, HolidaysAndFestivalsPlan
from .serializers import AvatarSerializer, SiteSerializer, UserSerializer, AccessKeySerializer, ProfileSerializer, UserHolidaysAndFestivalsSerializer, UserHolidaysAndFestivalsPlanSerializer


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class AccessKeyViewSet(viewsets.ModelViewSet):
    queryset = AccessKey.objects.all()
    serializer_class = AccessKeySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class HolidaysAndFestivalsViewSet(viewsets.ModelViewSet):
    queryset = HolidaysAndFestivals.objects.all()
    serializer_class = UserHolidaysAndFestivalsSerializer


class HolidaysAndFestivalsPlanViewSet(viewsets.ModelViewSet):
    queryset = HolidaysAndFestivalsPlan.objects.all()
    serializer_class = UserHolidaysAndFestivalsPlanSerializer
