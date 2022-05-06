
from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name="projects"),
    path('project/<str:pk>/', views.project, name="project"),
    path('create-project/', views.createProject, name="create-project"),
    path('query/', views.query, name="query"),
    path("get_answer/", views.get_answer, name = "get_answer"),
    path('queries/', views.queries, name="queries"),
    path('get_projects/', views.get_projects_api, name="get_projects"),
    path('get_queries/', views.get_queries_api, name="get_queries"),
    path('show_query/<str:pk>/', views.show_query, name="show_query"),
    path('toggle_activation/<str:pk>/', views.toggle_activation, name="toggle_activation"),
]