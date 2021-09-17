from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import render


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSimpleSerializer
    queryset = User.objects.all()


class MessageCreateAPIView(CreateAPIView):
    serializer_class = MessageSimpleSerializer
    queryset = Message.objects.all()


class BuildingCreateAPIView(CreateAPIView):
    serializer_class = BuildingSimpleSerializer
    queryset = Building.objects.all()


class HallCreateAPIView(CreateAPIView):
    serializer_class = HallSimpleSerializer
    queryset = Hall.objects.all()


class SignUpCreateAPIView(CreateAPIView):
    serializer_class = SignUp
    queryset = SignUp.objects.all()


class ClubCreateAPIView(CreateAPIView):
    serializer_class = ClubSimpleSerializer
    queryset = Club.objects.all()


class WorkoutCreateAPIView(CreateAPIView):
    serializer_class = WorkoutSimpleSerializer
    queryset = Workout.objects.all()


class PresenceCreateAPIView(CreateAPIView):
    serializer_class = PresenceSimpleSerializer
    queryset = Presence.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSimpleSerializer
    queryset = User.objects.all()


class MessageUpdateAPIView(UpdateAPIView):
    serializer_class = MessageSimpleSerializer
    queryset = Message.objects.all()


class BuildingUpdateAPIView(UpdateAPIView):
    serializer_class = BuildingSimpleSerializer
    queryset = Building.objects.all()


class HallUpdateAPIView(UpdateAPIView):
    serializer_class = HallSimpleSerializer
    queryset = Hall.objects.all()


class SignUpUpdateAPIView(UpdateAPIView):
    serializer_class = SignUp
    queryset = SignUp.objects.all()


class ClubUpdateAPIView(UpdateAPIView):
    serializer_class = ClubSimpleSerializer
    queryset = Club.objects.all()


class WorkoutUpdateAPIView(UpdateAPIView):
    serializer_class = WorkoutSimpleSerializer
    queryset = Workout.objects.all()


class PresenceUpdateAPIView(UpdateAPIView):
    serializer_class = PresenceSimpleSerializer
    queryset = Presence.objects.all()

class TrainingsForUser(APIView):
    def get(self, request, user_id):
        trainings = SignUp.objects.filter(user=user_id)
        serializer = SignUpSerializer(trainings, many=True)
        return Response({"Trainings: ", serializer.data})