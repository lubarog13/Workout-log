from rest_framework import serializers
from .models import *
from fcm_django.models import FCMDevice


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserNotAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'second_name', 'date_birth', 'sex', 'club']


class MessageSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class CoachSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = "__all__"


class BuildingSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"


class HallSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = "__all__"


class ClubSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"


class SignUpSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = "__all__"


class WorkoutSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = "__all__"


class PresenceSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    club = ClubSimpleSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'second_name', 'date_birth', 'sex', 'club']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserNotAllFieldsSerializer(many=False)
    recipient = UserNotAllFieldsSerializer(many=False)

    class Meta:
        model = Message
        fields = "__all__"


class CoachSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Coach
        fields = "__all__"


class HallSerializer(serializers.ModelSerializer):
    building = BuildingSimpleSerializer(many=False)

    class Meta:
        model = Hall
        fields = "__all__"


class ClubSerializer(serializers.ModelSerializer):
    coach = CoachSerializer(many=False)
    building = BuildingSimpleSerializer(many=False)

    class Meta:
        model = Club
        fields = "__all__"


class SignUpSerializer(serializers.ModelSerializer):
    club = ClubSerializer(many=False)
    user = UserNotAllFieldsSerializer(many=False)

    class Meta:
        model = SignUp
        fields = "__all__"


class WorkoutSerializer(serializers.ModelSerializer):
    hall = HallSerializer(many=False)
    club = ClubSerializer(many=False)
    coach_replace = CoachSerializer(many=False)

    class Meta:
        model = Workout
        fields = "__all__"


class PresenceSerializer(serializers.ModelSerializer):
    user = UserNotAllFieldsSerializer(many=False)
    workout = WorkoutSerializer(many=False)

    class Meta:
        model = Presence
        fields = "__all__"


class PresenceSimplerSerializer(serializers.ModelSerializer):
    user = UserNotAllFieldsSerializer(many=False)

    class Meta:
        model = Presence
        fields = "__all__"


class AnalysisPresenceCount(serializers.ModelSerializer):
    pcount = serializers.IntegerField()
    workout__club__id = serializers.IntegerField()

    class Meta:
        model = Presence
        fields = ('workout__club__id', 'pcount')


class AnalysisPresenceCountForMonths(serializers.ModelSerializer):
    pcount = serializers.IntegerField()
    workout__club__group = serializers.CharField()

    class Meta:
        model = Presence
        fields = ('workout__club__group', 'pcount')


class AnalysisWorkoutCount(serializers.ModelSerializer):
    wcount = serializers.IntegerField()
    club__group = serializers.CharField()

    class Meta:
        model = Workout
        fields = ('club__group', 'wcount')


class PresenceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presence
        fields = ('is_attend', 'reason')


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = "__all__"
