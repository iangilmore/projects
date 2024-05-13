from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    level = models.CharField(
        max_length=1,
        choices=[
            ('B', 'Beginner'),
            ('I', 'Intermediate'),
            ('A', 'Advanced'),
        ],
        default='B',
    )
    years_experience = models.IntegerField()
    
    def __str__(self):
      return self.name