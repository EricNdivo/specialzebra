from django.db import models

class ZebraQuery(models.Model):
    input_value = models.CharField(max_length=100)  
    input_type = models.CharField(max_length=20, choices=[('name', 'Name'), ('twitter', 'Twitter'), ('instagram', 'Instagram')])
    for_education = models.BooleanField(default=True)  
    consent_given = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.input_value} ({self.input_type})"

class ZebraResult(models.Model):
    query = models.ForeignKey(ZebraQuery, on_delete=models.CASCADE, related_name='results')
    source = models.CharField(max_length=50)  
    data = models.JSONField()  
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.query.input_value}"
    
