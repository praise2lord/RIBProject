from django.contrib import admin
from .models import SuspectCriminalRecord, RIBHeadquarter,RIBStation,StationUser, Reporter, Crime ,  Answer, QuestionSuspect , QuestionReporter, CAQS,CAQW,Case, Officer, Evidence, Suspect, Admin, Sector , Province , District


# Register your models here.
admin.site.register(RIBHeadquarter),
admin.site.register(RIBStation),
admin.site.register(StationUser),
admin.site.register(Case),
admin.site.register(Officer),
admin.site.register(Evidence), 
admin.site.register(Suspect),
admin.site.register(SuspectCriminalRecord),
admin.site.register(Admin), 
admin.site.register(Reporter),
admin.site.register(Province), 
admin.site.register(District),
admin.site.register(Sector),
# admin.site.register(Cell),
# admin.site.register(Village),
admin.site.register(QuestionSuspect),
admin.site.register(QuestionReporter),
admin.site.register(Answer),
admin.site.register(Crime),
admin.site.register(CAQS),
admin.site.register(CAQW),


