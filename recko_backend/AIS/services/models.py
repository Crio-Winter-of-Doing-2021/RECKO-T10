from django.db import models




class Accounts(models.Model):
    id=models.AutoField(primary_key=True)
    accountName=models.CharField(max_length=400)
    accountId=models.IntegerField()
    amount=models.DecimalField(max_digits=15, decimal_places=3)
    date=models.DateField()
    accountType=models.CharField(max_length=6)
    providerName=models.CharField(max_length=20)
    
    def __str__(self):
        return "{}-{}-{}-{}".format(self.id,self.accountName,self.accountType,self.amount)

