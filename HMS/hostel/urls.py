from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.Login,name='login'),
    path('verify_login',views.verify_login,name='verify_login'),
    path('signup',views.Signup,name='signup'),
    path("verify_otp",views.verify_otp,name="verify_otp"),
    path('verify',views.verify,name='verify'),
    path('verify_login',views.verify_login,name='verify_login'),
    path('student-dashboard',views.student_dashboard,name='student-dashboard'),
    path('admin-dashboard',views.admin_dashboard,name='admin-dashboard'),
    path('rector-dashboard',views.rector_dashboard,name='rector-dashboard'),
    path('mark-attendance', views.mark_attendance, name='mark_attendance'),
    path('logout', views.logout, name='logout'),
    path('complaints', views.complaints, name='complaints'),
    path('complaint_submit',views.complaints_submit, name='complaint_submit'),
]