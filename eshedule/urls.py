from django.urls import path, include, re_path
from eshedule.views import *

urlpatterns = [
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
    path('user/<int:user_id>/workouts/', SignUpsForUser.as_view())
]