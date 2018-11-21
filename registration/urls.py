from django.urls import path
from .views import SignupView, SignupVeteView, ProfileUpdate, EmailUpdate

urlpatterns = [
    path('signup/', SignupView.as_view(), name="signup"),
    path('veterinaria/signup/', SignupVeteView.as_view(), name="signup"),
    path('perfil/', ProfileUpdate.as_view(), name="profile"),
    path('perfil/email/', EmailUpdate.as_view(), name="profile_email"),
]