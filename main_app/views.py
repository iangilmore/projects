from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from .models import Project, Link, Language
from .serializers import UserSerializer, ProjectSerializer, LinkSerializer, LanguageSerializer


class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the projects API home route!'}
    return Response(content)


# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })


class LanguageList(generics.ListCreateAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer


class LanguageDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Language.objects.all()
  serializer_class = LanguageSerializer
  lookup_field = 'language_id'

class ProjectList(generics.ListCreateAPIView):
  serializer_class = ProjectSerializer
  permission_classes = [permissions.IsAuthenticated]
  
  def get_queryset(self):
    user = self.request.user
    return Project.objects.filter(user=user)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
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
  
  def perform_update(self, serializer):
    project = self.get_object()
    if project.user != self.request.user:
      raise PermissionDenied({"message": "You do not have permission to edit this project."})
    serializer.save()
  
  def perform_destroy(self, instance):
    if instance.user != self.request.user:
      raise PermissionDenied({"message": "You do not have permission to delete this project."})
    instance.delete()


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