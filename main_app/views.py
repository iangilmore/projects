from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Project, Link, Language
from .serializers import ProjectSerializer, LinkSerializer, LanguageSerializer

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the projects API home route!'}
    return Response(content)


class LanguageList(generics.ListCreateAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer


class LanguageDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer
  lookup_field = 'language_id'

class ProjectList(generics.ListCreateAPIView):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Project.objects.all()
  serializer_class = ProjectSerializer
  lookup_field = 'project_id'
  
  def get_queryset(self):
    user = self.request.user
    return Project.objects.filter(user=user)
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    
    languages_not_associated = Language.objects.exclude(id__in=instance.languages.all())
    languages_serializer = LanguageSerializer(languages_not_associated, many=True)
    
    return Response({
      'project': serializer.data,
      'languages_not_associated': languages_serializer.data
      })


class ProjectLanguage(APIView):
  
  def post(self, request, project_id, language_id):
    project = Project.objects.get(id=project_id)
    language = Language.objects.get(id=language_id)
    project.languages.add(language)
    return Response({'message': f'{language.name} added to {project.name}'})
  
  def delete(self, request, project_id, language_id):
    project = Project.objects.get(id=project_id)
    language = Language.objects.get(id=language_id)
    project.languages.remove(language)
    return Response({'message': f'{language.name} removed from {project.name}'})

class LinkList(generics.ListCreateAPIView):
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