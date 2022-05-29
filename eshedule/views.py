import djoser.urls.base
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from .serializers import *
from rest_framework.permissions import IsAdminUser
import datetime
from dateutil.parser import parse
from django.db.models import Q, QuerySet, Count
from rest_framework.response import Response
from fcm_django.models import FCMDevice
import requests
from django.core import mail
from django.contrib.auth.password_validation import validate_password
from djoser.views import UserViewSet
import random
import string
from pyfcm import FCMNotification
from django.template import Context as cont
from django.template.loader import get_template

push_service = FCMNotification(api_key="AAAAOUUqqfM:APA91bGumWRwEjq9pvfcFza32yWVZe_LymLdb0Ga4IGzwIISC0ZVsECTPWM-UAlvqwLFWP8wot8456VCaXFqu8zsJ64o37_8LRR3jHr1zKfOz0vhrkGylwD7un6XlyuPaeqDATp7r3xa")
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
    permission_classes = [IsAdminUser]


class HallCreateAPIView(CreateAPIView):
    serializer_class = HallSimpleSerializer
    queryset = Hall.objects.all()
    permission_classes = [IsAdminUser]


class SignUpCreateAPIView(CreateAPIView):
    serializer_class = SignUp
    queryset = SignUp.objects.all()


class ClubCreateAPIView(APIView):
    def post(self, request):
        characters = string.ascii_letters + string.digits
        request.data['identifier'] = ''.join(random.choice(characters) for i in range(21))
        serializer = ClubSimpleSerializer(data=request.data)
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
        signup1 = SignUp.objects.filter(club__identifier=request.data['identifier'])\
            .filter(user__id=request.data['user'])
        if signup1:
            if signup1[0].end_date < dt_e:
                signup1[0].end_date = dt_e
            signup1[0].save()
            serializer = SignUpSerializer(signup1[0], many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            signup = SignUp(club=club, user=user, start_date=dt, end_date=dt_e)
            signup.save()
            serializer = SignUpSerializer(signup, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SignupForUserCreate(APIView):
    def post(self, request):
        serializer = SignUpSimpleSerializer(data=request.data)
        today = datetime.datetime.now()
        if serializer.is_valid():
            serializer.save()
            club = Club.objects.get(pk=request.data['club'])
            workouts = Workout.objects.filter(club=club.id, start_time__gte=today)
            user = User.objects.get(pk=request.data['user'])
            for workout in workouts:
                presence = Presence(user=user, workout=workout, is_attend=None, reason=None, delay=False, early_ret=False)
                presence.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkoutCreateAPIView(APIView):

    def post(self, request):
        serializer = WorkoutSimpleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            club = Club.objects.get(pk=request.data['club'])
            group = User.objects.filter(club=club.id)
            for user in group:
                presence = Presence(user=user, workout=Workout.objects.get(pk=serializer.data['id']), is_attend=None, reason=None, delay=False, early_ret=False)
                presence.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresenceCreateAPIView(CreateAPIView):
    serializer_class = PresenceSimpleSerializer
    queryset = Presence.objects.all()


class CoachCreateAPIView(APIView):

    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user = User.objects.get(username=request.data['username'])
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.is_coach = True
        user.save()
        coach = Coach(post=request.data['post'], user=user)
        coach.save()
        return Response(status=status.HTTP_201_CREATED)


class PresenceUpdateByUserID(APIView):

    def patch(self, request, user_id, workout_id):
        try:
            if request.data['reason'] is not None:
                Presence.objects.filter(user=user_id, workout=workout_id).update(reason=request.data['reason'])
                return Response(status=status.HTTP_201_CREATED)
            if request.data['is_attend'] == 'true' or request.data['is_attend'] == True:
                Presence.objects.filter(user=user_id, workout=workout_id).update(is_attend=True)
                return Response(status=status.HTTP_201_CREATED)
            elif request.data['is_attend'] == 'false' or request.data['is_attend'] == False:
                Presence.objects.filter(user=user_id, workout=workout_id).update(is_attend=False)
                return Response(status=status.HTTP_201_CREATED)
        except:
            if request.data['is_attend'] == 'true' or request.data['is_attend'] == True:
                Presence.objects.filter(user=user_id, workout=workout_id).update(is_attend=True)
                return Response(status=status.HTTP_201_CREATED)
            elif request.data['is_attend'] == 'false' or request.data['is_attend'] == False:
                Presence.objects.filter(user=user_id, workout=workout_id).update(is_attend=False)
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # except Exception:
        #     print(Exception)
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


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


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserNotAllFieldsSerializer
    queryset = User.objects.all()


class ClubUpdateAPIView(UpdateAPIView):
    serializer_class = ClubSimpleSerializer
    queryset = Club.objects.all()


class WorkoutUpdateAPIView(APIView):
    def put(self, request, pk, format=None):
        workout = Workout.objects.get(pk=pk)
        serializer = WorkoutSimpleSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.data['is_carried_out'] == 'true':
                presences = Presence.objects.filter(workout=workout.pk)
                for presence in presences:
                    presence.is_attend = None
                    presence.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PresenceUpdateAPIView(APIView):
    def put(self, request, pk, format=None):
        presence = Presence.objects.get(pk=pk)
        workout = Workout.objects.get(pk=presence.workout.pk)
        if workout.is_carried_out:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = PresenceSimpleSerializer(presence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        messages = Message.objects.filter(recipient=user_id).order_by('-send_time')
        serializer = MessageSerializer(messages, many=True)
        return Response({"Messages":serializer.data})


class MessagesFromUserAPiView(APIView):

    def get(self, request, user_id):
        messages = Message.objects.filter(sender=user_id).order_by('-send_time')
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
        idx = (today.weekday()) % 7
        mun = today - datetime.timedelta(idx)
        print(mun)
        return mun

    @staticmethod
    def find_next_monday():
       today = datetime.date.today()
       idx = (today.weekday()) % 7
       mun = today + datetime.timedelta(7-idx)
       print(mun)
       return mun

    def get(self, request, user_id):
        l_m = self.find_last_monday()
        workouts = Workout.objects.filter(start_time__lt=self.find_next_monday()).filter(start_time__gte=l_m).filter(user__id=user_id).order_by('start_time')
        serializer = WorkoutSerializer(workouts, many=True)
        for data in serializer.data:
            data['on_train'] = Presence.objects.filter(workout=data['id']).filter(is_attend=True).count()
            data['dont_know'] = Presence.objects.filter(workout=data['id']).filter(is_attend__isnull=True).count()
            data['not_on_train'] = Presence.objects.filter(workout=data['id']).filter(is_attend=False).count()
            go = Presence.objects.filter(workout=data['id']).filter(user=user_id)[0]
            if go.is_attend==True:
                data['is_on'] = True
            elif go.is_attend==False:
                data['is_on'] = False
            else:
                data['is_on'] = None
        return Response({"Workouts": serializer.data})


class WorkoutsOnWeekForCoach(APIView):

    @staticmethod
    def find_last_monday():
        today = datetime.date.today()
        idx = (today.weekday()) % 7
        mun = today - datetime.timedelta(idx)
        print(mun)
        return mun

    @staticmethod
    def find_next_monday():
       today = datetime.date.today()
       idx = (today.weekday()) % 7
       mun = today + datetime.timedelta(7-idx)
       print(mun)
       return mun

    def get(self, request, coach_id):
        l_m = self.find_last_monday()
        workouts = Workout.objects.filter(start_time__lt=self.find_next_monday()).filter(start_time__gte=l_m).filter(
            Q(coach_replace__id=coach_id) | Q(club__coach__id=coach_id))
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
        presences = Presence.objects.filter(workout__start_time__day=day).filter(Q(workout__club__coach=coach_id) | Q(workout__coach_replace=coach_id)).filter(workout__start_time__month=month).filter(workout__start_time__year=year).order_by('user__last_name').order_by('user__first_name')
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


class PresenceCountInMonthForTypes(APIView):

    def get(self, request, user_id, month):
        user = User.objects.get(pk=user_id)
        if not user.is_coach:
            cardio = Presence.objects.filter(user=user_id).filter(workout__type='кардио', workout__start_time__month=month).filter(is_attend=True).count()
            silov = Presence.objects.filter(user=user_id).filter(workout__type='силовая', workout__start_time__month=month).filter(is_attend=True).count()
            for_tech = Presence.objects.filter(user=user_id).filter(workout__type='на технику', workout__start_time__month=month).filter(
                is_attend=True).count()
            for_all = Presence.objects.filter(user=user_id).filter(workout__type='общая', workout__start_time__month=month).filter(is_attend=True).count()
            another = Presence.objects.filter(user=user_id).filter(workout__type='другое', workout__start_time__month=month).filter(
                is_attend=True).count()
        else:
            cardio = Workout.objects.filter(club__coach__user=user_id, start_time__month=month).filter(type='кардио').filter(
                Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            silov = Workout.objects.filter(club__coach__user=user_id, start_time__month=month).filter(type='силовая').filter(
                Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            for_tech = Workout.objects.filter(club__coach__user=user_id, start_time__month=month).filter(type='на технику').filter(
                Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            for_all = Workout.objects.filter(club__coach__user=user_id, start_time__month=month).filter(type='общая').filter(
                Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            another = Workout.objects.filter(club__coach__user=user_id, start_time__month=month).filter(type='другое').filter(
                Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
        return Response(
            {"Cardio": cardio, "Strength": silov, "For_tech": for_tech, "For_all": for_all, "Another": another})


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
        presences = Presence.objects.filter(workout__start_time__month=month).filter(user=user_id)
        serializer = PresenceSerializer(presences, many=True)
        return Response({"Presences": serializer.data})


class CoachDetailAPIView(RetrieveAPIView):
    serializer_class = CoachSerializer
    queryset = Coach.objects.all()


class PresencesCountForTypes(APIView):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        if not user.is_coach:
            cardio = Presence.objects.filter(user=user_id).filter(workout__type='кардио').filter(is_attend=True).count()
            silov = Presence.objects.filter(user=user_id).filter(workout__type='силовая').filter(is_attend=True).count()
            for_tech = Presence.objects.filter(user=user_id).filter(workout__type='на технику').filter(is_attend=True).count()
            for_all = Presence.objects.filter(user=user_id).filter(workout__type='общая').filter(is_attend=True).count()
            another = Presence.objects.filter(user=user_id).filter(workout__type='другое').filter(is_attend=True).count()
        else:
            cardio = Workout.objects.filter(club__coach__user=user_id).filter(type='кардио').filter(Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            silov = Workout.objects.filter(club__coach__user=user_id).filter(type='силовая').filter(Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            for_tech = Workout.objects.filter(club__coach__user=user_id).filter(type='на технику').filter(Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            for_all = Workout.objects.filter(club__coach__user=user_id).filter(type='общая').filter(Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
            another = Workout.objects.filter(club__coach__user=user_id).filter(type='другое').filter(Q(is_carried_out=False) & Q(start_time__lte=datetime.datetime.now())).count()
        return Response({"Cardio": cardio, "Strength": silov, "For_tech": for_tech, "For_all": for_all, "Another": another})


class PresencesForMounth(APIView):

    def get(self, request, user_id, month, year):
        presences = Presence.objects.filter(user=user_id).filter(workout__start_time__month=month, workout__start_time__year=year)
        serializer = PresenceSerializer(presences, many=True)
        return Response({"Presences": serializer.data})

class WorkoutsForMonth(APIView):
    def get(self, request, user_id, month, year):
        workouts =  Workout.objects.filter(user__id=user_id).filter(start_time__month=month, start_time__year=year)
        serializer = WorkoutSerializer(workouts, many=True)
        for data in serializer.data:
            data['on_train'] = Presence.objects.filter(workout=data['id']).filter(is_attend=True).count()
            data['dont_know'] = Presence.objects.filter(workout=data['id']).filter(is_attend__isnull=True).count()
            data['not_on_train'] = Presence.objects.filter(workout=data['id']).filter(is_attend=False).count()
        return Response({"Workouts": serializer.data})
    
    
class WorkoutsForMounth(APIView):
    
    def get(self, request, coach_id, month, year):
        workouts = Workout.objects.filter(Q(coach_replace=coach_id) | Q(club__coach=coach_id)).filter(start_time__month=month).filter(start_time__year=year)
        serializer = WorkoutSerializer(workouts, many=True)
        return Response({"Workouts": serializer.data})


class PresencesCountForMonths(APIView):

    def get(self, request, user_id, year):
        presences = []
        user = User.objects.get(pk=user_id)
        for i in range (1,13):
            if not user.is_coach:
                presence = Presence.objects.filter(user=user_id).filter(is_attend=True).filter(workout__start_time__month=i).filter(workout__start_time__year=year).count()
            else:
                presence = Workout.objects.filter(club__coach__user=user_id).filter(Q(start_time__month=i) & Q(start_time__year=year)).count()
            presences.append(presence)
        return Response({"jan": presences[0], "feb": presences[1], "mar": presences[2], "apr": presences[3]
                            , "may": presences[4], "jun": presences[5], "jul": presences[6], "aug": presences[7],
                         "sep": presences[8], "oct": presences[9], "nov": presences[10], "dec": presences[11]})


class NotAttendCountForMonths(APIView):
    def get(self, request, user_id, year):
        presences = []
        user = User.objects.get(pk=user_id)
        for i in range (1,13):
            if not user.is_coach:
                presence = Presence.objects.filter(user=user_id).filter(is_attend=False).filter(workout__start_time__month=i).filter(workout__start_time__year=year).count()
            presences.append(presence)
        return Response({"jan": presences[0], "feb": presences[1], "mar": presences[2], "apr": presences[3]
                            , "may": presences[4], "jun": presences[5], "jul": presences[6], "aug": presences[7],
                         "sep": presences[8], "oct": presences[9], "nov": presences[10], "dec": presences[11]})


class PresenceCountForGroups(APIView):
    # Select group, count(presence) from presence join workout on presence.workout_id=workout.workout_id join club on club.club_id=workout.workout_id where coach_id = coach_id and is_attend=true group by group
    def post(self, request, coach_id):
        if  request.data['day']=='all' :
            counts = Presence.objects.select_related('workout')\
                .select_related('club').filter(workout__club__coach=coach_id)\
                .filter(is_attend=True).values('workout__club__id')\
                .annotate(pcount=Count('is_attend'))
        else:
            counts = Presence.objects.select_related('workout')\
                .select_related('club').filter(workout__club__coach=coach_id)\
                .filter(is_attend=True).filter(workout__start_time__week_day=request.data['day']).values('workout__club__id')\
                .annotate(pcount=Count('is_attend'))
            print(request.data['day'])
        serializer = AnalysisPresenceCount(counts, many=True)
        return Response({"Stat": serializer.data})


class PresenceCountForGroupsForMonth(APIView):
    # Select group, count(presence) from presence join workout on presence.workout_id=workout.workout_id join club on club.club_id=workout.workout_id where coach_id = coach_id and is_attend=true group by group
    def post(self, request, coach_id):
        if  request.data['day']=='all' :
            counts = Presence.objects.select_related('workout')\
                .select_related('club').filter(workout__club__coach=coach_id)\
                .filter(is_attend=True).values('workout__club__group')\
                .annotate(pcount=Count('is_attend'))
        else:
            counts = Presence.objects.select_related('workout')\
                .select_related('club').filter(workout__club__coach=coach_id)\
                .filter(is_attend=True).filter(workout__start_time__month=request.data['day']).values('workout__club__group')\
                .annotate(pcount=Count('is_attend'))
        serializer = AnalysisPresenceCountForMonths(counts, many=True)
        return Response({"Stat": serializer.data})

class WorkoutCountForGroupForTypes(APIView):
    def get(self, request, coach_id, club_id):
        cardio = Workout.objects.filter(Q(club__coach__id=coach_id) | Q(coach_replace=coach_id)).filter(club=club_id).filter(type='кардио').count()
        silov = Workout.objects.filter(Q(club__coach__id=coach_id) | Q(coach_replace=coach_id)).filter(club=club_id).filter(type='силовая').count()
        for_tech = Workout.objects.filter(Q(club__coach__id=coach_id) | Q(coach_replace=coach_id)).filter(club=club_id).filter(type='на технику').count()
        for_all = Workout.objects.filter(Q(club__coach__id=coach_id) | Q(coach_replace=coach_id)).filter(club=club_id).filter(type='общая').count()
        another = Workout.objects.filter(Q(club__coach__id=coach_id) | Q(coach_replace=coach_id)).filter(club=club_id).filter(type='другое').count()
        return Response({"Cardio": cardio, "Strength": silov, "For_tech": for_tech, "For_all": for_all, "Another": another})


class WorkoutCountForGroups(APIView):

    def post(self, request, coach_id):
        if request.data['day'] == 'all':
            counts = Workout.objects.select_related('club').filter(club__coach=coach_id)\
                .filter(start_time__lte=datetime.datetime.now())\
                .values('club__group').annotate(wcount=Count('id'))
        else:
            counts = Workout.objects.select_related('club').filter(club__coach=coach_id) \
                .filter(start_time__lte=datetime.datetime.now()).filter(start_time__week_day=request.data['day']) \
                .values('club__group').annotate(wcount=Count('id'))
        serializer = AnalysisWorkoutCount(counts, many=True)
        return Response({"Stat": serializer.data})


class WorkoutCountForGroupsForMonth(APIView):

    def post(self, request, coach_id):
        if request.data['day'] == 'all':
            counts = Workout.objects.select_related('club').filter(club__coach=coach_id)\
                .filter(start_time__lte=datetime.datetime.now())\
                .values('club__group').annotate(wcount=Count('id'))
        else:
            counts = Workout.objects.select_related('club').filter(club__coach=coach_id) \
                .filter(start_time__lte=datetime.datetime.now()).filter(start_time__month=request.data['day']) \
                .values('club__group').annotate(wcount=Count('id'))
        serializer = AnalysisWorkoutCount(counts, many=True)
        return Response({"Stat": serializer.data})



class UsersInClub(APIView):

    def get(self, request, club_id):
        users = User.objects.filter(club__id=club_id)
        serializer = UserNotAllFieldsSerializer(users, many=True)
        return Response({"Users": serializer.data})

class WorkoutListAPIView(ListAPIView):
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()


class UserSearch(APIView):

    def post(self, request):
        print(request.data)
        name = request.data['username']
        names = name.split()
        user = User.objects.filter(Q(username=name) | Q(email=name))
        if len(user) != 0:
            serializer = UserNotAllFieldsSerializer(user, many=True)
            return Response({"Users": serializer.data})
        if len(names) == 3:
            user = User.objects.filter(last_name=names[0], first_name=names[1], second_name=names[2])
            if len(user) != 0:
                serializer = UserNotAllFieldsSerializer(user, many=True)
                return Response({"Users": serializer.data})
        if len(names) == 2:
             user = User.objects.filter(last_name=names[0], first_name=names[1])
             if len(user) != 0:
                 serializer = UserNotAllFieldsSerializer(user, many=True)
                 return Response({"Users": serializer.data})
        return Response(status=status.HTTP_404_NOT_FOUND)


class SignupDeleteAPIView(APIView):

    def delete(self, request, sign_up_id):
        signUP = SignUp.objects.get(pk=sign_up_id)
        today = datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day, 0, 0, 0, 0)
        if signUP is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        Presence.objects.filter(user__id=signUP.user.pk).filter(workout__start_time__gt=today).delete()
        signUP.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoachForUserAPIView(APIView):

    def get(self, request, user_id):
        coach = Coach.objects.get(user__id=user_id)
        serializer = CoachSerializer(coach, many=False)
        return Response({"Coach": serializer.data})


class SendNotification(APIView):

    def post(self, request):
        users = User.objects.filter(club__id=request.data['club'])
        message_title = request.data['title']
        message_body = request.data['message']
        registrations_ids = []
        print('ok1')
        for user in users:
            for fcm_device in FCMDevice.objects.filter(user_id=user.id):
                registrations_ids.append(fcm_device.registration_id)
        print(registrations_ids)
        result = push_service.notify_multiple_devices(registration_ids=registrations_ids, message_title=message_title,message_body=message_body)
        print(result)
        return Response({"Result": result})

class DevicesListForUser(APIView):

    def get(self, request, user_id):
        devices = FCMDevice.objects.filter(user_id=user_id)
        serializer = FCMDeviceSerializer(devices, many=True)
        return Response({'Devices': serializer.data})


class CreateDevice(CreateAPIView):
    serializer_class = FCMDeviceSerializer
    queryset = FCMDevice.objects.all()


class UpdateDevice(UpdateAPIView):
    serializer_class = FCMDeviceSerializer
    queryset = FCMDevice.objects.all()


class ResetPassword(APIView):

    def post(self, request):
        username = request.data['username']
        user = User.objects.get(username=username)
        connection = mail.get_connection()
        plaintext = get_template('email.txt')
        htmly = get_template('email.html')
        print(user.email)
        connection.open()
        print(user)
        if user.reset_password_token is None:
            characters = string.ascii_letters + string.digits
            user.reset_password_token = ''.join(random.choice(characters) for i in range(21))
            user.save()
        d = cont({'username': user.username, 'token': user.reset_password_token})
        text_content = plaintext.render(d.flatten())
        html_content = htmly.render(d.flatten())
        email1 = mail.EmailMultiAlternatives(
            'Восстановление пароля',
            text_content,
            User.objects.get(username='admin').email,
            [user.email],
            connection=connection,
        )
        email1.attach_alternative(html_content, "text/html")
        email1.send()
        print(user)
        connection.close()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewPassword(APIView):

    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        if user.reset_password_token == request.data['reset_password_token']:
            # p_S = UserViewSet
            # p_S.me(p_S, request=request)
            request1 = request
            print("{0}://{1}/".format(request.scheme, request.get_host()))
            r = requests.patch("{0}://{1}/auth/users/me/".format(request1.scheme, request1.get_host()), data=request1.data, headers=request1.headers)
            return Response(status=status.HTTP_200_OK)
            # try:
            #     user.save()
            # except :
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NewPasswordByDjoser(View):

    def get(self, request, uid, token):
        context = {'uid': uid, 'token': token}
        return render(request, 'reset_password.html', context)


class UploadBuildingImage(APIView):

    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST' and request.data['image_file']:
            upload = request.data['image_file']
            fss = FileSystemStorage()
            try:
                building_id = request.data['building_id']
            except:
                building_id = None
            if building_id:
                building = Building.objects.get(pk=building_id)
            else:
                building = Building.objects.all().last()
            name = (building.pk).__str__() + "_building.jpg"
            if fss.exists(name):
                fss.delete(name)
            file = fss.save(name, upload)
            file_url = fss.url(file)
            return Response({'Path': file_url}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UploadHallImage(APIView):

    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST' and request.data['image_file']:
            upload = request.data['image_file']
            fss = FileSystemStorage()
            try:
                hall_id = request.data['hall_id']
            except:
                hall_id = None
            if hall_id:
                hall = Hall.objects.get(pk=hall_id)
            else:
                hall = Hall.objects.all().last()
            name = (hall.pk).__str__() + "_hall.jpg"
            if fss.exists(name):
                fss.delete(name)
            file = fss.save(name, upload)
            file_url = fss.url(file)
            return Response({'Path': file_url}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UploadCoachImage(APIView):

    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST' and request.data['image_file']:
            upload = request.data['image_file']
            fss = FileSystemStorage()
            try:
                coach_id = request.data['coach_id']
            except:
                coach_id = None
            if coach_id:
                coach = Coach.objects.get(pk=coach_id)
            else:
                coach = Coach.objects.all().last()
            name = (coach.pk).__str__() + "_coach.jpg"
            if fss.exists(name):
                fss.delete(name)
            file = fss.save(name, upload)
            file_url = fss.url(file)
            return Response({'Path': file_url}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BuildingAPIView(RetrieveAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSimpleSerializer
