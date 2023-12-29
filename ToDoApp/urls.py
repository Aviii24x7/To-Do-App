from  django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete,CustomLoginView, UserRegister, complete_task
from django.contrib.auth.views import LogoutView


urlpatterns = [
    
    path('login/', CustomLoginView.as_view(), name = "user-login-page"),
    path('logout/', LogoutView.as_view(next_page="user-login-page"), name= "user-logout-page"),
    path('register/', UserRegister.as_view(), name = "user-register-page"),
    path('', TaskList.as_view(), name = "tasks-page"),
    path('task-<int:pk>/',TaskDetail.as_view(), name = "task-detail-page"),
    path('task-create/', TaskCreate.as_view(), name = "task-create-page"),
    path('task-update-<int:pk>/',TaskUpdate.as_view(), name = "task-update-page"),
    path('task-delete-<int:pk>/',TaskDelete.as_view(), name = "task-delete-page"),
    path('/<int:pk>', complete_task, name='task-complete'),
    
    
]