from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from .serializers import *
import datetime
from dateutil.parser import parse
from django.db.models import Q, QuerySet, Count
from rest_framework.response import Response
import random
import string
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


class ClubCreateAPIView(APIView):
    def post(self, request):
        # remember old state
        _mutable = request.data._mutable
        # set to mutable
        request.data._mutable = True
        characters = string.ascii_letters + string.digits
        request.data['identifier'] = ''.join(random.choice(characters) for i in range(21))
        serializer = ClubSimpleSerializer(data=request.data)
        request.data._mutable = _mutable
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpCreate(APIView):
    def post(self, request):
        club = Club.objects.get(identifier=request.data['identifier'])
        user = User.objects.get(pk=request.data['user'])
        try:
            dt = parse(request.data['start_date']).date()
            dt_e = parse(request.data['end_date']).date()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        signup = SignUp(club=club, user=user, start_date=dt, end_date=dt_e)
        signup.save()
        serializer = SignUpSimpleSerializer(signup, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class WorkoutCreateAPIView(CreateAPIView):
    serializer_class = WorkoutSimpleSerializer
    queryset = Workout.objects.all()


class PresenceCreateAPIView(CreateAPIView):
    serializer_class = PresenceSimpleSerializer
    queryset = Presence.objects.all()


class CoachCreateAPIView(CreateAPIView):
    serializer_class = CoachSimpleSerializer
    queryset = Coach.objects.all()


class CoachUpdateAPIView(UpdateAPIView):
    serializer_class = CoachSimpleSerializer
    queryset = Coach.objects.all()


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


class SignUpsForUser(APIView):

    def get(self, request, user_id):
        trainings = SignUp.objects.filter(user=user_id)
        serializer = SignUpSerializer(trainings, many=True)
        return Response({"Sign_Ups":serializer.data})


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
        return Response({"Clubs":serializer.data})


class ClubsInBuildingAPIView(APIView):

    def get(self, request, building_id):
        clubs = Club.objects.filter(building=building_id)
        serializer = ClubSerializer(clubs, many=True)
        return Response({"Clubs":serializer.data})


class MessagesForUserAPiView(APIView):

    def get(self, request, user_id):
        messages = Message.objects.filter(recipient=user_id)
        serializer = MessageSerializer(messages, many=True)
        return Response({"Messages":serializer.data})


class MessagesFromUserAPiView(APIView):

    def get(self, request, user_id):
        messages = Message.objects.filter(sender=user_id)
        serializer = MessageSerializer(messages, many=True)
        return Response({"Messages":serializer.data})


class WorkoutsForCoach(APIView):

    def get(self, request, coach_id):
        clubs = Club.objects.filter(coach=coach_id)
        workouts = Workout.objects.filter(Q(club__in=clubs) | Q(coach_replace=coach_id))
        serializer = WorkoutSerializer(workouts, many=True)
        return Response({"Workouts":serializer.data})


class WorkoutsOnWeekForUser(APIView):

    @staticmethod
    def find_last_monday():
        today = datetime.date.today()
        idx = (today.weekday() + 1) % 7
        mun = today - datetime.timedelta(7 - idx)
        return mun

    @staticmethod
    def find_next_monday():
       today = datetime.date.today()
       idx = (today.weekday()+1) % 7
       mun = today + datetime.timedelta(7-idx)
       return mun

    def get(self, request, user_id):
        l_m = self.find_last_monday()
        workouts = Workout.objects.filter(start_time__lt=self.find_next_monday()).filter(start_time__gte=l_m).filter(user__id=user_id)
        serializer = WorkoutSerializer(workouts, many=True)
        for data in serializer.data:
            data['on_train'] = Presence.objects.filter(workout=data['id']).filter(is_attend=True).count()
            data['dont_know'] = Presence.objects.filter(workout=data['id']).filter(is_attend__isnull=True).count()
            data['not_on_train'] = Presence.objects.filter(workout=data['id']).filter(is_attend=False).count()
        return Response({"Workouts": serializer.data})


class HallsInBuildingAPIView(APIView):

    def get(self, request, building_id):
        halls = Hall.objects.filter(building=building_id)
        serializer = HallSerializer(halls, many=True)
        return Response({'Halls': serializer.data})


class UserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TodayWorkoutsForUser(APIView):

    def get(self, request, user_id):
        today = datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day, 0, 0, 0, 0)
        tomorrow = today + datetime.timedelta(1)
        workouts = Workout.objects.filter(start_time__gte=today).filter(start_time__lt=tomorrow).filter(user__id=user_id)
        serializer = WorkoutSerializer(workouts, many=True)
        return Response({"Workouts": serializer.data})

class PresenceForWorkout(APIView):

    def get(self, request, workout_id):
        presences = Presence.objects.filter(workout=workout_id)
        serializer = PresenceSimplerSerializer(presences, many=True)
        return Response({"Presences": serializer.data})


class PresencesOnDay(APIView):

    def get(self, request, coach_id, day, month, year):
        presences = Presence.objects.filter(workout__start_time__day=day).filter(workout__club__coach=coach_id).filter(workout__start_time__month=month).filter(workout__start_time__year=year).order_by('user__last_name').order_by('user__first_name')
        serializer = PresenceSerializer(presences, many=True)
        return Response({"Presences": serializer.data})


class WorkoutsOnDay(APIView):

    def get(self, request, user_id, day, month, year):
        workouts = Workout.objects.filter(start_time__day=day).filter(club__signup__user=user_id).filter(start_time__month=month).filter(start_time__year=year).order_by('start_time')
        serializer = WorkoutSerializer(workouts, many=True)
        return Response({"Workouts": serializer.data})


class MessageDeleteAPIView(DestroyAPIView):
    serializer_class = MessageSimpleSerializer
    queryset = Message.objects.all()


class PresenceCountInMonth(APIView):

    def get(self, request, user_id, month):
        presences = Presence.objects.filter(user=user_id).filter(workout__start_time__month=month).filter(is_attend=True).count()
        return Response({"Count": presences})


class MessageDetailAPIView(RetrieveAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class HallDetailAPIView(RetrieveAPIView):
    serializer_class = HallSerializer
    queryset = Hall.objects.all()


class ClubsForTrainerAPIView(APIView):

    def get(self, request, coach_id):
        clubs = Club.objects.filter(coach=coach_id)
        serializer = ClubSerializer(clubs, many=True)
        return Response({'Clubs': serializer.data})
    
   
class PresencesInMonth(APIView):

    def get(self, request, user_id, month):
        presences = Presence.objects.filter(worcout__start_time__month=month).filter(user=user_id)
        serializer = PresenceSerializer(presences, many=True)
        return Response({"Presences": serializer.data})


class CoachDetailAPIView(RetrieveAPIView):
    serializer_class = CoachSerializer
    queryset = Coach.objects.all()


class PresencesCountForTypes(APIView):

    def get(self, request, user_id):
        cardio = Presence.objects.filter(user=user_id).filter(workout__type='кардио').filter(is_attend=True).count()
        silov = Presence.objects.filter(user=user_id).filter(workout__type='силовая').filter(is_attend=True).count()
        for_tech = Presence.objects.filter(user=user_id).filter(workout__type='на технику').filter(is_attend=True).count()
        for_all = Presence.objects.filter(user=user_id).filter(workout__type='общая').filter(is_attend=True).count()
        another = Presence.objects.filter(user=user_id).filter(workout__type='другое').filter(is_attend=True).count()
        return Response({"Cardio": cardio, "Strength": silov, "For_tech": for_tech, "For_all": for_all, "Another": another})


class PresencesForMounth(APIView):

    def get(self, request, user_id, month, year):
        presences = Presence.objects.filter(user=user_id).filter(workout__start_time__month=month, workout__start_time__year=year)
        serializer = PresenceSimplerSerializer(presences, many=True)
        return Response({"Presences": serializer.data})


class PresencesCountForMonths(APIView):

    def get(self, request, user_id, year):
        presences = []
        for i in range (1,13):
            presence = Presence.objects.filter(user=user_id).filter(is_attend=True).filter(workout__start_time__month=i).filter(workout__start_time__year=year).count()
            presences.append(presence)
        return Response({"jan": presences[0], "feb": presences[1], "mar": presences[2], "apr": presences[3]
                            , "may": presences[4], "jun": presences[5], "jul": presences[6], "aug": presences[7],
                         "sep": presences[8], "oct": presences[9], "nov": presences[10], "dec": presences[11]})