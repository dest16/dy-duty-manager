from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Avatar, Site, AccessKey, Profile, User, HolidaysAndFestivals, HolidaysAndFestivalsPlan


class AvatarSerializer(serializers.ModelSerializer):
    image = serializers.CharField()

    class Meta:
        model = Avatar
        fields = ('pk', 'image',)


class SiteSerializer(serializers.ModelSerializer):
    url = serializers.CharField()

    class Meta:
        model = Site
        fields = ('pk', 'url',)


class AccessKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessKey
        fields = ('pk', 'key',)


class ProfileSerializer(WritableNestedModelSerializer):
    # Direct ManyToMany relation
    sites = SiteSerializer(many=True)

    # Reverse FK relation
    avatars = AvatarSerializer(many=True)

    # Direct FK relation
    access_key = AccessKeySerializer(allow_null=True)

    class Meta:
        model = Profile
        fields = ('pk', 'sites', 'avatars', 'access_key',)


class UserSerializer(WritableNestedModelSerializer):
    # Reverse OneToOne relation
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('pk', 'profile', 'username',)


class UserHolidaysAndFestivalsPlanSerializer(WritableNestedModelSerializer):

    class Meta:
        model = HolidaysAndFestivalsPlan
        exclude = ['festival']


class UserHolidaysAndFestivalsSerializer(WritableNestedModelSerializer):
    # Reverse FK relation
    plan = UserHolidaysAndFestivalsPlanSerializer(many=True)

    class Meta:
        model = HolidaysAndFestivals
        fields = ('id', 'date', 'name', 'plan')

