from django.forms import ModelForm
from django import forms
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SuspectCriminalRecord,Crime,CAQS,CAQW,Answer,QuestionSuspect,QuestionReporter,StationUser, Case,Suspect,Evidence,RIBStation,Officer,Reporter
from django.core.validators import RegexValidator

class RibOfficerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
    def __init__(self, *args, **kwargs):
        super(RibOfficerRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super(RibOfficerRegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user



class StationNameRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        
    def __init__(self, *args, **kwargs):
        super(StationNameRegistrationForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text = None
    def save(self, commit=True):
        user = super(StationNameRegistrationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user


class DateInput(forms.DateInput):
    input_type = 'date'

class CaseForm(forms.ModelForm):
    victim_age =forms.DateField(widget=DateInput)
    
    class Meta:
        model = Case
        # fields = '__all__'
        fields = ('case_name','crimeType','victim_name','reporter_name','victim_age','reporter_phone','victim_address','case_desc','stationuser', 'suspects','reporter_email')
        stationuser = forms.ModelChoiceField(queryset=User.objects.none(), required=True)
        
        labels = {
            'case_name':'Case Name',
            'crimeType':'Type Of Crime',
            'victim_name':'Victim Name',
            'victim_age':'Victim Aage',
            'reporter_name':'Reporter Name',
            'reporter_phone':'Reporter Phone(+250 *********)',
            'victim_address':'Address of the Victim',
            'case_desc':'Case Description',
            'stationuser':'Case Officer',
            'reporter_email':'Repoter Email',
            }
        
        widgets = {
            'case_name': forms.TextInput(attrs={'placeholder':'Case name in brief'}),
            }

class RibstationForm(forms.ModelForm):
    class Meta:
        model = RIBStation
        fields = ('user','station_name','province')
        labels = {
            'user':'Station Commander',
            'station_name':'Station Name',
            'province':'Province',
            }

class SuspectForm(forms.ModelForm):
    dob =forms.DateField(widget=DateInput)
    class Meta:
        model = SuspectCriminalRecord
        model = Suspect
        # fields = '__all__'
        fields = ('suspectNID','f_name','l_name','gender','dob','phone','relation','father_name','mother_name','province','district','cell','village','suspectimage','note')
        labels = {
            'suspectNID':'Suspect National Id',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'dob':'Date Of Birth',
            'phone':'Phone Number',            
            'relation':'Suspect Relation with Crime',
            'father_name':'Father Name',
            'mother_name':'Mother Name',
            'province':'Province',
            'district':'District',
            'cell':'Cell',
            'village':'Village',
            # 'ribstation':'RIBStation',
            'suspectimage':'Suspect Photo',
            'note':'Short Note',
            }

class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ('title','evidenceCategory','evidence_note','evidencerimage','level')
        labels = {
            'evidenceCategory':'Evidence Category',
            'evidencerimage':'Evidence Photo',
            'level':'Evidence level',
            'evidence_note':'Short note',
            }

class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
        # fields = '__all__'
        fields = ('user','OfficerNationalId','f_name','l_name','gender','phone','email','rank','recruit_year','officerimage')
        labels = {
            'user':'User Name',
            'OfficerNationalId':'Officer ID',
            'f_name':'Fist Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'phone':'Phone',
            'email':'Email',
            'rank':'Rank',
            'recruit_year':'Join RIB Year',
            # 'ribstation' : 'RIB POST',
            'officerimage':'Officer Photo',
            }

class RibCommanderForm(forms.ModelForm):
    class Meta:
        model = Officer
        # fields = '__all__'
        fields = ('user','OfficerNationalId','f_name','l_name','gender','phone','email','rank','recruit_year','ribstation','officerimage')
        labels = {
            'user':'User Name',
            'OfficerNationalId':'Commander NID',
            'f_name':'Fist Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'phone':'Phone',
            'email':'Email',
            'rank':'Rank',
            'recruit_year':'Join RIB Year',
            'ribstation' : 'RIB POST',
            'officerimage':'Officer Photo',
            }
class StationUserForm(forms.ModelForm):
    class Meta:
        model = StationUser
        # fields = '__all__'
        fields = ('user','nationalId','f_name','l_name','gender','phone','email','rank','recruit_year','ribstation','officerimage')
        labels = {
            'user':'User Name',
            'nationalId':'Officer ID',
            'f_name':'Fist Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'phone':'Phone',
            'email':'Email',
            'rank':'Rank',
            'recruit_year':'Join RIB Year',
            'ribstation' : 'RIB POST',
            'officerimage':'Officer Photo',
            }

class ReporterForm(forms.ModelForm):
    class Meta:
        model = Reporter
        # fields = '__all__'
        fields = ('reporterNID','f_name','l_name','gender','email','phone','relation','vote','note')
        labels = {
            'reporterNID':'Reporter Id',
            'f_name':'First Name',
            'l_name':'Last Name',
            'gender':'Gender',
            'email':'Email',
            'phone':'Phone Number',            
            'relation':'Your Relation with suspect',
            'vote':'Are you linking suspect to the case(Guilty)',
            'note':'Short Note',
            # 'suspect':'Who are you Reporting',
            }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionSuspect
        fields = ('questionId','questionName','crimeType')
        labels = {
            'questionId': 'Id of the Question',
            'questionName':'Describe the Question To Be Asked Suspects',
            'crimeType':'Crime Category',
            }
        widgets = {
            'questionId': forms.TextInput(attrs={'placeholder':'Question ID'}),
            'questionName': forms.Textarea(attrs={'placeholder':'Question To be asked'})
        }

class QuestionRepoForm(forms.ModelForm):
    class Meta:
        model = QuestionReporter
        fields = ('questionId','questionName','crimeType')
        labels = {
            'questionId': 'Id of the Question',
            'questionName':'Describe the Question To Be Asked Witness',
            'crimeType':'Crime Category',
            }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('AnswerName',)
        labels = {
            'AnswerName':'Predict an Answer To Be Answered',
            }

class CAQSForm(forms.ModelForm):
    class Meta:
        model = CAQS
        fields = ('suspect','question','answer')
        labels = {
            'suspect':'What is your name? ',
            'question':'Question',
            'answer':'Your Answer',

            
            }

class CAQWForm(forms.ModelForm):
    class Meta:
        model = CAQW
        fields = ('witness','question','answer')
        labels = {
            'witness':'What is your name? ',
            'question':'Question',
            'answer':'Your Answer',

            
            }
            

class CrimeForm(forms.ModelForm):
    class Meta:
        model = Crime
        fields = ('crimeName',)
        labels = {
            'crimeName':'Describe the Crime Name',
            }