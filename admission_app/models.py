from django.db import models

class Admission(models.Model):
    gre = models.FloatField()
    toefl = models.FloatField()
    cgpa = models.FloatField()
    sop = models.FloatField()
    lor = models.FloatField()
    research = models.IntegerField()
    chance = models.FloatField()

    def __str__(self):
        return f"GRE: {self.gre}, CGPA: {self.cgpa}"
    
class ModelHistory(models.Model):
    model_name = models.CharField(max_length=100)
    r2 = models.FloatField()
    mse = models.FloatField()
    mae = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name    