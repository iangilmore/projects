from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    # url = models.URLField()
    # level = models.CharField(
    #     max_length=1,
    #     choices=[
    #         ('B', 'Beginner'),
    #         ('I', 'Intermediate'),
    #         ('A', 'Advanced'),
    #     ],
    #     default='B',
    # )
    # years_experience = models.IntegerField()
    
    def __str__(self):
      return self.name

class Link(models.Model):
    type = models.CharField(
      choices=[
        ('Live Demo', 'Live Demo'),
        ('Deployment', 'Deployment'),
        ('Source Repository', 'Source Repository'),
        ('Frontend Source Repository', 'Frontend Source Repository'),
        ('Backend Source Repository', 'Backend Source Repository'),
        ('Wireframes', 'Wireframes'),
        ('ERD', 'ERD'),
        ('Component Hierachy Diagram', 'Component Hierachy Diagram'),
        ('Custom', 'Custom')
      ]
      )
    custom_type = models.CharField(
      max_length=50,
      blank=True
      )
    url = models.URLField()
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
      return f"A {self.type} link to {self.url}"