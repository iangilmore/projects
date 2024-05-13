from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Skill
from .serializers import SkillSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the skill-tracker API home route!'}
    return Response(content)

class SkillList(generics.ListCreateAPIView):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer

class SkillDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer
  lookup_field = 'id'