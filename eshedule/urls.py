from django.urls import path, include, re_path
from eshedule.views import *
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('buildings/', BuildingListAPIView.as_view()),
    path('halls/', HallListAPIView.as_view()),
    path('building/<int:building_id>/halls/', HallsInBuildingAPIView.as_view()),
    path('coaches/', CoachesListAPIView.as_view()),
    path('clubs/', ClubListAPIView.as_view()),
    path('building/<int:building_id>/clubs/', ClubsInBuildingAPIView.as_view()),
    path('coach/<int:coach_id>/clubs/', ClubForCoachAPIView.as_view()),
    path('user/<int:pk>/', UserAPIView.as_view()),
    path('user/<int:user_id>/sign_ups/', SignUpsForUser.as_view()),
    path('user/<int:user_id>/week_workouts/', WorkoutsOnWeekForUser.as_view()),
    path('user/<int:user_id>/today_workouts/', TodayWorkoutsForUser.as_view()),
    path('workout/<int:workout_id>/presences/', PresenceForWorkout.as_view()),
    path('user/<int:user_id>/workouts/<int:day>/<int:month>/<int:year>/', WorkoutsOnDay.as_view()),
    path('coach/<int:coach_id>/presences/<int:day>/<int:month>/<int:year>/', PresencesOnDay.as_view()),
    path('user/craete/', UserCreateAPIView.as_view()),
    path('club/create/', ClubCreateAPIView.as_view()),
    path('coach/create/', CoachCreateAPIView.as_view()),
    path('signup/create/', SignUpCreate.as_view()),
    path('workout/create/', WorkoutCreateAPIView.as_view()),
    path('presence/create/', PresenceCreateAPIView.as_view()),
    path('message/create/', MessageCreateAPIView.as_view()),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view()),
    path('club/<int:pk>/update/', ClubUpdateAPIView.as_view()),
    path('coach/<int:pk>/update/', CoachUpdateAPIView.as_view()),
    path('workout/<int:pk>/update/', WorkoutUpdateAPIView.as_view()),
    path('presence/<int:pk>/update/', PresenceUpdateAPIView.as_view()),
    path('message/<int:pk>/update/', MessageUpdateAPIView.as_view()),
    path('message/<int:pk>/delete/', MessageDeleteAPIView.as_view()),
    path('user/<int:user_id>/messages/send/', MessagesFromUserAPiView.as_view()),
    path('user/<int:user_id>/messages/', MessagesForUserAPiView.as_view()),
    path('message/<int:pk>/', MessageDetailAPIView.as_view()),
    path('hall/<int:pk>/', HallDetailAPIView.as_view()),
    path('coach/<int:coach_id>/clubs/', ClubForCoachAPIView.as_view()),
    path('user/<int:user_id>/presences/count/<int:month>/', PresenceCountInMonth.as_view()),
    path('user/<int:user_id>/workouts/presences/<int:month>/', PresencesInMonth.as_view()),
    path('coach/<int:pk>/', CoachDetailAPIView.as_view()),
    path('user/<int:user_id>/analysis/types/', PresencesCountForTypes.as_view()),
    path('user/<int:user_id>/presences/month/<int:month>/<int:year>', PresencesForMounth.as_view()),
    path('user/<int:user_id>/analysis/<int:year>/', PresencesCountForMonths.as_view())
]