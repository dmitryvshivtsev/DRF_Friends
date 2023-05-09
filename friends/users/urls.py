from django.urls import include, path
from users.views import Register, send_request, accept_request, reject_request


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(template_name='registration/register.html'), name='register'),
    path('add-friend/<int:id>/', send_request, name='add-friend'),
    path('accept/<int:id>/', accept_request, name='accept'),
    path('reject/<int:id>/', reject_request, name='reject'),
]
