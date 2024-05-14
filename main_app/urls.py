from django.urls import path
# import Home view from the views file
from .views import Home, ProjectList, ProjectDetail, LinkListCreate, LinkDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('projects/', ProjectList.as_view(), name='project-list'),
  path('projects/<int:id>/', ProjectDetail.as_view(), name='project-detail'),
  path('projects/<int:project_id>/links/', LinkListCreate.as_view(), name='link-list-create'),
  path('projects/<int:project_id>/links/<int:link_id>/', LinkDetail.as_view(), name='link-detail'),
]