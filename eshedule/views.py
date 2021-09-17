from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from .serializers import *
import datetime
from django.db.models import Q
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


class BuildingListAPIView(ListAPIView):
    serializer_class = BuildingSimpleSerializer
    queryset = Building.objects.all()


class CoachesListAPIView(ListAPIView):
    serializer_class = CoachSerializer
    queryset = Coach.objects.all()


class HallListAPIView(ListAPIView):
    serializer_class = HallSerializer
    queryset = Hall.objects.all()


class ClubListAPIView(ListAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.all()


class ClubForCoachAPIView(APIView):

    def get(self, request, coach_id):
        clubs = Club.objects.filter(coach=coach_id)
        serializer = ClubSerializer(clubs, many=True)
        return Response({"Clubs: ", serializer.data})


class ClubsInBuildingAPIView(APIView):

    def get(self, request, building_id):
        clubs = Club.objects.filter(building=building_id)
        serializer = ClubSerializer(clubs, many=True)
        return Response({"Clubs: ", serializer.data})


class MessagesForUserAPiView(APIView):

    def get(self, request, user_id):
        messages = Message.objects.filter(recipient=user_id)
        serializer = MessageSerializer(messages, many=True)
        return Response({"Messages: ", serializer.data})


class MessagesFromUserAPiView(APIView):

    def get(self, request, user_id):
        messages = Message.objects.filter(sender=user_id)
        serializer = MessageSerializer(messages, many=True)
        return Response({"Messages: ", serializer.data})


class WorkoutsForCoach(APIView):

    def get(self, request, coach_id):
        clubs = Club.objects.filter(coach=coach_id)
        workouts = Workout.objects.filter(Q(club__in=clubs) | Q(coach_replace=coach_id))
        serializer = WorkoutSerializer(workouts, many=True)
        return Response({"Workouts: ", serializer.data})


class WorkoutsOnWeekForUser(APIView):

    @staticmethod
    def find_next_monday():
       today = datetime.date.today()
       idx = (today.weekday()+1) % 7
       mun = today + datetime.timedelta(7-idx)
       return mun

    def get(self, request, user_id):
        workouts = Workout.objects.filter(start_time__gt=self.find_next_monday()).filter(user__id=user_id)
        serializer = WorkoutSerializer(workouts, many=True)
        return Response({"Workouts: ", serializer.data})
      
