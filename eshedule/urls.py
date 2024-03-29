from django.urls import path, include, re_path
from django.conf.urls.static import static

from eshedule.views import *

from trainingLog import settings

urlpatterns = [
                  path('auth/', include('djoser.urls')),
                  re_path(r'^auth/', include('djoser.urls.authtoken')),
                  path('buildings/', BuildingListAPIView.as_view()),
                  path('halls/', HallListAPIView.as_view()),
                  path('building/create/', BuildingCreateAPIView.as_view()),
                  path('building/<int:building_id>/halls/', HallsInBuildingAPIView.as_view()),
                  path('user/<int:pk>/', UserDetailAPIView.as_view()),
                  path('coaches/', CoachesListAPIView.as_view()),
                  path('building/<int:pk>/', BuildingAPIView.as_view()),
                  path('building/<int:pk>/update/', BuildingUpdateAPIView.as_view()),
                  path('clubs/', ClubListAPIView.as_view()),
                  path('building/<int:building_id>/clubs/', ClubsInBuildingAPIView.as_view()),
                  path('coach/<int:coach_id>/clubs/', ClubForCoachAPIView.as_view()),
                  path('user/<int:pk>/', UserAPIView.as_view()),
                  path('user/<int:user_id>/sign_ups/', SignUpsForUser.as_view()),
                  path('user/<int:user_id>/week_workouts/', WorkoutsOnWeekForUser.as_view()),
                  path('hall/create/', HallCreateAPIView.as_view()),
                  path('hall/<int:pk>/update/', HallUpdateAPIView.as_view()),
                  path('user/<int:user_id>/today_workouts/', TodayWorkoutsForUser.as_view()),
                  path('presence/update/user/<int:user_id>/workout/<int:workout_id>/',
                       PresenceUpdateByUserID.as_view()),
                  path('workout/<int:workout_id>/presences/', PresenceForWorkout.as_view()),
                  path('user/<int:user_id>/workouts/<int:day>/<int:month>/<int:year>/', WorkoutsOnDay.as_view()),
                  path('coach/<int:coach_id>/presences/<int:day>/<int:month>/<int:year>/', PresencesOnDay.as_view()),
                  path('user/craete/', UserCreateAPIView.as_view()),
                  path('club/create/', ClubCreateAPIView.as_view()),
                  path('coach/create/', CoachCreateAPIView.as_view()),
                  path('signup/create/', SignUpCreate.as_view()),
                  path('coach/signup/create/', SignupForUserCreate.as_view()),
                  path('workout/create/', WorkoutCreateAPIView.as_view()),
                  path('presence/create/', PresenceCreateAPIView.as_view()),
                  path('message/create/', MessageCreateAPIView.as_view()),
                  path('user/<int:pk>/update/', UserUpdateAPIView.as_view()),
                  path('club/<int:pk>/update/', ClubUpdateAPIView.as_view()),
                  path('coach/<int:pk>/update/', CoachUpdateAPIView.as_view()),
                  path('workout/<int:pk>/update/', WorkoutUpdateAPIView.as_view()),
                  path('presence/<int:pk>/update/', PresenceUpdateAPIView.as_view()),
                  path('coach/<int:coach_id>/week_workouts/', WorkoutsOnWeekForCoach.as_view()),
                  path('message/<int:pk>/update/', MessageUpdateAPIView.as_view()),
                  path('message/<int:pk>/delete/', MessageDeleteAPIView.as_view()),
                  path('user/<int:user_id>/messages/send/', MessagesFromUserAPiView.as_view()),
                  path('user/<int:user_id>/messages/', MessagesForUserAPiView.as_view()),
                  path('message/<int:pk>/', MessageDetailAPIView.as_view()),
                  path('hall/<int:pk>/', HallDetailAPIView.as_view()),
                  path('coach/<int:coach_id>/clubs/', ClubForCoachAPIView.as_view()),
                  path('user/<int:user_id>/presences/count/<int:month>/', PresenceCountInMonthForTypes.as_view()),
                  path('user/<int:user_id>/workouts/presences/<int:month>/', PresencesInMonth.as_view()),
                  path('user/<int:user_id>/workouts/<int:month>/<int:year>/', WorkoutsForMonth.as_view()),
                  path('coach/<int:pk>/', CoachDetailAPIView.as_view()),
                  path('user/<int:user_id>/analysis/types/', PresencesCountForTypes.as_view()),
                  path('user/<int:user_id>/presences/month/<int:month>/<int:year>/', PresencesForMounth.as_view()),
                  path('user/<int:user_id>/analysis/<int:year>/', PresencesCountForMonths.as_view()),
                  path('user/<int:user_id>/analysis/not_attend/<int:year>/', NotAttendCountForMonths.as_view()),
                  path('coach/<int:coach_id>/workouts/<int:month>/<int:year>/', WorkoutsForMounth.as_view()),
                  path('coach/<int:coach_id>/analysis/groups/presences/', PresenceCountForGroups.as_view()),
                  path('coach/<int:coach_id>/analysis/club/<int:club_id>/workouts/', WorkoutCountForGroupForTypes.as_view()),
                  path('coach/<int:coach_id>/analysis/groups/workouts/', WorkoutCountForGroups.as_view()),
                  path('coach/<int:coach_id>/analysis/groups/month/', WorkoutCountForGroupsForMonth.as_view()),
                  path('coach/<int:coach_id>/analysis/groups/presences/month/', PresenceCountForGroupsForMonth.as_view()),
                  path("workouts/", WorkoutListAPIView.as_view()),
                  path('club/<int:club_id>/users/', UsersInClub.as_view()),
                  path('search/user/', UserSearch.as_view()),
                  path("signup/<int:sign_up_id>/delete/", SignupDeleteAPIView.as_view()),
                  path("coach/user<int:user_id>/", CoachForUserAPIView.as_view()),
                  path("send_message/", SendNotification.as_view()),
                  path("fcmdevice/create/", CreateDevice.as_view()),
                  path("fcmdevice/<int:pk>/update/", UpdateDevice.as_view()),
                  path("user/<int:user_id>/fcmdevices/", DevicesListForUser.as_view()),
                  path("reset_password/", ResetPassword.as_view()),
                  path("new_password/", NewPassword.as_view(), name="new_password"),
                  path("email/reset/confirm/<uid>/<token>", NewPasswordByDjoser.as_view()),
                  path("upload/building/", UploadBuildingImage.as_view(), name="upload"),
                  path("upload/hall/", UploadHallImage.as_view()),
                  path("upload/coach/", UploadCoachImage.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
