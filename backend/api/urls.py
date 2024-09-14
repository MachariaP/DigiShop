from django.urls import path

from userauths import views as userauths_views


urlpatterns = [
    path('user/token/', userauths_views.myTokenObtainPairView.as_view(), name='token_obtain_pair')
]