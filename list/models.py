from django.db import models

# Create your models here.

class list(models.Model):
    date = models.TextField(null=True)
    title = models.TextField(null=True)
    count = models.TextField(null=True)
    link = models.TextField(null=True)
    image = models.TextField(null=True)

    def __str__(self):
        return self.title


#class Poll(models.Model):
#    start_date = models.DateTimeField()
#    end_date = models.DateTimeField()
#    area = models.CharField(max_length=15)

#class Choice(models.Model):
#    poll = models.ForeignKey(Poll,on_delete=models.CASCADE,)
#    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,)
#    votes = models.IntegerField(default=0)