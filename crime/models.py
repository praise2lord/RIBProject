from django.db import models
from django.contrib.auth.models import User
import africastalking
from datetime import datetime

# Create your models here.

GENDER = [
    ("M", "MALE"),
    ("F", "FEMALE"),
]

SUSPECTSTATUS = [
    ("free", "free"),
    ("freeFromCase", "freeFromCase"),    
    ("middle", "middle"),
    ("middleFromCase", "middleFromCase"),    
    ("primary_suspect", "primary_suspect"),
]

LEVEL_CHOICES = [
    ('Easy', 'Easy'),
    ('Middle', 'Middle'),
    ('Difficult', 'Difficult'),
    ]

EVIDENCECATEGORY = [
    ("Physical", "Physical"),
    ("Logical", "Logical"),
]

RANKCOMMANDER = [
    ("AssistantSuperintendentofPolice", "Assistant Superintendent of Police"),
    ("InspectorOfPolice", "Inspector of Police"),
    ("AssistantInspectorOfPolice", "Assistant Inspector of Police"),  
]

RANK = [
    ("Sergeant", "Sergeant"),
    ("Corporal", "Corporal"),
    ("Police Constable", "Police Constable"),
    ("Civilian", "Civilian"),
    
]



CRIMETYPE = [
    ("Robbery", "Robbery"),
    ("Violent", "Violent"),
    ("Murder", "Murder"),
    ]
STATUS = [
    ("Pending", "Pending"),
    ("Studied", "Studied"),
    ("Finished", "Finished"), 
    ("Deleted", "Deleted"),
]
VOTE = [
    ("Yes", "YES"),
    ("No", "NO"),
]

WHERE = [
    ("I was there at crime scene", "I was there at crime scene"),
    ("I were at work", "I were at work"),
    ("I was Near the crime scene", "I was Near the crime scene"),
    ("I was Too Far in different district", "I was Too Far in different district"),
]

REASON = [
    ("I was there", "I was there"),
    ("I don't know", "I don't know"),
    ("I know the Victim", "I know the Victim"),
    ("I've met with the Victim", "I've met with the Victim"),
]

class Province(models.Model):
    prov_name = models.CharField(max_length=30)

    def __str__(self):
        return self.prov_name


class District(models.Model):
    dist_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.dist_name

class Sector(models.Model):
    sect_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.sect_name

# class Cell(models.Model):
#     cel_name = models.CharField(max_length=30)
    
#     def __str__(self):
#         return self.cel_name

# class Village(models.Model):
#     vil_name = models.CharField(max_length=30)
    
#     def __str__(self):
#         return self.vil_name



class RIBStation(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=30, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    def __str__(self):
        return self.station_name


class Officer(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    OfficerNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    officerimage = models.ImageField(upload_to='images/', default="upload/anonymous-user.png", max_length=154, blank=True, null=True)
    rank = models.CharField(max_length=100, choices=RANKCOMMANDER)
    recruit_year = models.IntegerField()
    ribstation = models.ForeignKey(RIBStation, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.f_name 

class Evidence(models.Model):
    title =  models.CharField(max_length=100, blank=False, null=False, default='')
    evidenceCategory = models.CharField(max_length=15, choices=EVIDENCECATEGORY, default="Select Category")
    evidence_note = models.TextField(max_length=255)
    level =  models.CharField(max_length=30, blank=False, choices=LEVEL_CHOICES, default='')
    evidencerimage = models.ImageField(upload_to='upload/', null=True, blank=True , default="upload/anonymous-user.png",)
    def __str__(self):
        return self.title
        
class Reporter(models.Model):
    reporterNID = models.CharField(max_length=16, unique=True, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    email = models.CharField(max_length=30, blank=False)
    phone =  models.CharField(max_length=10, blank=False)
    relation = models.CharField(max_length=30, blank=False)   
    vote = models.CharField(max_length=3, choices=VOTE)
    note = models.TextField(max_length=100, blank=True)
    
  
    def __str__(self):
        return self.f_name  



class StationUser(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    nationalId = models.CharField(max_length=16, blank=True, null=True,)
    f_name = models.CharField(max_length=30, blank=True, null=True,)
    l_name = models.CharField(max_length=30, blank=True, null=True,)
    gender = models.CharField(max_length=1, choices=GENDER,)
    phone = models.CharField(max_length=10, blank=True, null=True,)
    email = models.CharField(max_length=50, blank=True, null=True,)
    officerimage = models.ImageField(upload_to='upload/', default="upload/anonymous-user.png", blank=True, null=True)
    rank = models.CharField(max_length=100, choices=RANK, null=True,)
    recruit_year = models.IntegerField(null=True, blank=True)
    ribstation = models.ForeignKey(RIBStation, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.user.username

class Suspect(models.Model):
    suspectNID = models.CharField(max_length=16, unique=True, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=31, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    dob = models.DateField()
    phone =  models.CharField(max_length=10, blank=False)
    date_arrested = models.DateTimeField(auto_now_add=True,null=True) 
    date_released = models.DateTimeField(null=True) 
    relation = models.CharField(max_length=30, blank=False)   
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    crime_rate = models.FloatField(default=0) # over 50 marks
    witness_rate = models.FloatField(default=0) # over 50 marks
    evidence_rate = models.FloatField(default=0) # over 50 marks
    suspect_status = models.CharField(max_length=100, blank=False,choices=SUSPECTSTATUS, default='free')
    province = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    cell = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    note = models.TextField(max_length=150, blank=False)
    suspectimage = models.ImageField(upload_to='images/', default="upload/anonymous-user.png", max_length=154, blank=True, null=True)
    evidences = models.ManyToManyField(Evidence, blank=True, null=True)
    reporters = models.ManyToManyField(Reporter, blank=True, null=True)
    ribstation = models.ForeignKey(RIBStation, on_delete=models.CASCADE, null=True, blank=True)
    stationuser = models.ForeignKey(StationUser, on_delete=models.CASCADE, null=True, blank=True)
  
    def __str__(self):
        return self.f_name 

    @staticmethod
    def send_sms(phone_number , message):
        username = "tusifu"  # use 'sandbox' for development in the test environment
        api_key = "c1b79e7560de16b8aa9a43b7c31123f9b2148d4bb17a6d33a1dfcf95701f08b3"  # use your sandbox app API key for development in the test environment
        africastalking.initialize(username, api_key)
        # Initialize a service e.g. SMS
        sms = africastalking.SMS

        # Or use it asynchronously
        def on_finish(error, response):
            if error is not None:
                raise error
            print(response)
        response = sms.send(message, [phone_number], callback=on_finish)
        print(response)

class SuspectCriminalRecord(models.Model):
    suspectNID = models.CharField(max_length=16, unique=True, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    dob = models.DateField()
    phone =  models.CharField(max_length=10, blank=False)
    date_arrested = models.DateTimeField(auto_now_add=True,null=True) 
    relation = models.CharField(max_length=30, blank=False)   
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    cell = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    note = models.TextField(max_length=150, blank=False)
    evidences = models.ManyToManyField(Evidence, blank=True, null=True)
    reporters = models.ManyToManyField(Reporter, blank=True, null=True)
    ribstation = models.ForeignKey(RIBStation, on_delete=models.CASCADE, null=True, blank=True)
    stationuser = models.ForeignKey(StationUser, on_delete=models.CASCADE, null=True, blank=True)
  
    def __str__(self):
        return self.f_name  


class Crime(models.Model):
    
    crimeName = models.CharField(max_length=30, blank=False)
        
    def __str__(self):
        return self.crimeName 


class Case(models.Model):
    case_name = models.CharField(max_length=50)
    victim_name = models.CharField(max_length=90, blank=True, null=True)
    victim_age = models.DateField(blank=True, null=True)
    reporter_name = models.CharField(max_length=90, blank=True, null=True)
    reporter_phone = models.CharField(max_length=13, blank=True, null=True)
    victim_address = models.CharField(max_length=90, blank=True, null=True)
    crimeType = models.CharField(max_length=30,null=True, choices=CRIMETYPE)
    case_desc = models.TextField()
    stationuser = models.ForeignKey(StationUser, on_delete=models.CASCADE, null=True, blank=True)
    suspects = models.ManyToManyField(Suspect, blank=True, null=True)
    ribstation = models.ForeignKey(RIBStation, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS)
    case_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True,null=True)
    reporter_email = models.EmailField(max_length=100, blank=True, null=True)  # Email field

    
    def __str__(self):
        return self.case_number

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_case_number()                                 # calling the set_case_number function

    def set_case_number(self):
        if not self.case_number: 
            year = datetime.now().year                              # if case_number of the instance is blank
            # case_number = str(year)+"RIB"+ ribstation + "%05d" % (self.id ,)      # generating the case_number
            case_number = str(year)+"RIB"+ "%05d" % (self.id ,)      # generating the case_number
            
            case= Case.objects.get(id=self.id)     # getting the instance
            case.case_number = case_number                           # allocating the value
            case.save()




class Admin(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    adminNationalId = models.CharField(max_length=16, blank=False)
    f_name = models.CharField(max_length=30, blank=False)
    l_name = models.CharField(max_length=30, blank=False)
    gender = models.CharField(max_length=1, choices=GENDER)
    phone = models.CharField(max_length=10, blank=False)
    email = models.CharField(max_length=50, blank=False)
    adminimage = models.ImageField(upload_to='images/', default="upload/anonymous-user.png" ,max_length=154, blank=True, null=True)
    def __str__(self):
        return self.f_name 

class RIBHeadquarter(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=30, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
  
    
    def __str__(self):
        return self.station_name  


class QuestionSuspect(models.Model):
    questionId = models.CharField(max_length=4 ,null=True, unique=True, blank=True)
    questionName = models.TextField(blank=False)
    crimeType = models.CharField(max_length=40, blank=True, null=True, choices=CRIMETYPE)
        
    def __str__(self):
        return self.questionName 



class Answer(models.Model):
    
    AnswerName = models.TextField(default="not_applied",blank=False)
        
    def __str__(self):
        return self.AnswerName 

class CAQS(models.Model):
    
    question = models.ForeignKey(QuestionSuspect, on_delete=models.CASCADE, null=True, blank=True)
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
        
    # def __str__(self):
    #     return self.question

class QuestionReporter(models.Model):    
    questionId = models.CharField(max_length=4, null=True, unique=True, blank=True)
    questionName = models.TextField(blank=False)
    crimeType = models.CharField(max_length=40,null=True,blank=True, choices=CRIMETYPE)

        
    def __str__(self):
        return self.questionName 
        
class CAQW(models.Model):
    witness = models.ForeignKey(Reporter, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(QuestionReporter, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

# def __str__(self):
    #     return self.question