from django.urls import include, path
from users.views import *


urlpatterns = [
    path("all-users/", AllUsersView.as_view()),
    path("my-friends/", UserFriendsView.as_view()),
    path("incoming/", IncomingRequestsView.as_view()),
    path("outcoming/", OutcomingRequestsView.as_view()),
    path("befriend/<int:pk>/", SendFriendRequestView.as_view()),
    path("accept/<int:pk>/", AcceptFriendRequestView.as_view()),
    path("reject/<int:pk>/", RejectFriendRequestView.as_view()),
    path("unfriend/<int:pk>/", RemoveFriendView.as_view()),
    path("status/<int:pk>/", FriendStatusView.as_view()),
]
