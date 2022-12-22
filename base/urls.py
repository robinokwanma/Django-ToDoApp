from django.urls import path,include
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, TaskLogin, TaskLogout, TaskRegister

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('taskedit/<int:pk>/', TaskUpdate.as_view(), name='taskedit'),
    path('taskdelete/<int:pk>/', TaskDelete.as_view(), name='taskdelete'),
    path('form/', TaskCreate.as_view(), name='taskform'),
    path('login/', TaskLogin.as_view(), name='login'),
    path('register/', TaskRegister.as_view(), name='register'),
    path('loout/', TaskLogout.as_view(), name='logout'),
    # path('logout/', views.logout_user, name='logout'),
]