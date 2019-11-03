from django.db import models

# Create your models here.

class Candidate(models.Model):
    name = models.TextField(null=True)
    introduction = models.TextField()
    area = models.CharField(max_length=15)
    party_number = models.TextField(null=True)

    def __str__(self):
        return self.name


#class Poll(models.Model):
#    start_date = models.DateTimeField()
#    end_date = models.DateTimeField()
#    area = models.CharField(max_length=15)

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,)
#    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,)
#    votes = models.IntegerField(default=0)
