from rest_framework import serializers


class FileSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=100)
    file_path = serializers.CharField(max_length=250)
    rating = serializers.IntegerField(required=False,allow_null=True)
    verdict = serializers.CharField(max_length=500,required=False,allow_null=True,allow_blank=True)
    distance = serializers.FloatField(required=False,allow_null=True)


class PupilRequestSerializer(serializers.Serializer):

    age = serializers.CharField(max_length=10,required=False,allow_null=True,allow_blank=True)
    gender = serializers.CharField(max_length=10,required=False,allow_null=True,allow_blank=True)
    participantIndex = serializers.CharField(max_length=20,required=False,allow_null=True,allow_blank=True)
    phoneBrand = serializers.CharField(max_length=50,required=False,allow_null=True,allow_blank=True)
    phoneModel = serializers.CharField(max_length=50,required=False,allow_null=True,allow_blank=True)
    sleepTime = serializers.CharField(max_length=20,required=False,allow_null=True,allow_blank=True)
    files = serializers.ListField(
        child=FileSerializer(),
        default=list
    )

