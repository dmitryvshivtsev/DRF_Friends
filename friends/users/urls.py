from django.urls import include, path
from users.views import *


urlpatterns = [
    path('all-users/', AllUsersView.as_view()),
    path('my-friends/', UserFriendsView.as_view()),
    path('incoming/', IncomingRequestsView.as_view()),
    path('outcoming/', OutcomingRequestsView.as_view()),
    path('befriend/<int:id>/', SendFriendRequestView.as_view()),
    path('accept/<int:id>/', AcceptFriendRequestView.as_view()),
    path('reject/<int:id>/', RejectFriendRequestView.as_view()),
    path('unfriend/<int:id>', RejectFriendRequestView.as_view()),
]
