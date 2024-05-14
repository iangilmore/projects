from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Project, Link
from .serializers import ProjectSerializer, LinkSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the projects API home route!'}
    return Response(content)


class ProjectList(generics.ListCreateAPIView):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  lookup_field = 'id'


class LinkListCreate(generics.ListCreateAPIView):
  serializer_class = LinkSerializer
  
  def get_queryset(self):
    project_id = self.kwargs['project_id']
    return Link.objects.filter(project_id=project_id)
  
  def perform_create(self, serializer):
    project_id = self.kwargs['project_id']
    project = Project.objects.get(id=project_id)
    serializer.save(project=project)


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = LinkSerializer
  lookup_field = 'link_id'
  
  def get_queryset(self):
    project_id = self.kwargs['project_id']
    return Link.objects.filter(project_id=project_id)