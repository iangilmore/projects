from django.urls import path
# import Home view from the views file
from .views import Home, SkillList, SkillDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('skills/', SkillList.as_view(), name='skill-list'),
  path('skills/<int:id>/', SkillDetail.as_view(), name='skill-detail'),
]