from django.urls import path
# import Home view from the views file
from .views import Home, ProjectList, ProjectDetail, LinkList, LinkDetail, LanguageList, LanguageDetail, ProjectLanguage

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('projects/', ProjectList.as_view(), name='project-list'),
  path('projects/<int:id>/', ProjectDetail.as_view(), name='project-detail'),
  path('projects/<int:project_id>/links/', LinkList.as_view(), name='link-list'),
  path('projects/<int:project_id>/links/<int:link_id>/', LinkDetail.as_view(), name='link-detail'),
  path('languages/', LanguageList.as_view(), name='language-list'),
  path('languages/<int:id>/', LanguageDetail.as_view(), name='language-detail'),
  path('projects/<int:project_id>/languages/<int:language_id>', ProjectLanguage.as_view(), name='project-language')
]