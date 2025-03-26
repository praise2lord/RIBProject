from django.shortcuts import render, redirect 
from django.core.paginator import Paginator
from django.template.loader import get_template
from.utils  import render_to_pdf
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django .http import HttpResponse,JsonResponse
from .models import *
import datetime
from django.db.models import Count
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
from .forms import RibCommanderForm,CrimeForm,CAQSForm,CAQWForm,AnswerForm,QuestionForm,QuestionRepoForm,StationUserForm,RibOfficerRegistrationForm,CaseForm,SuspectForm,EvidenceForm,RibstationForm,OfficerForm,ReporterForm,StationNameRegistrationForm
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .filters import SuspectFilter
from collections import Counter
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def error401(request):

    context = {}
    return render(request, 'crime/StationOficer/401.html', context)

def errorDelete(request):

    context = {}
    return render(request, 'crime/RIBHQ/deleteRequest.html', context)

def errorDeleteCase(request, case_pk):
	case = Case.objects.get(id=case_pk) 
	case.status = 'Deleted'
	case.save()
	
	context = {'case':case}
	return render(request, 'crime/RIBStation/deleteRequest.html', context)

def errorUpdateCase(request):

    context = {}
    return render(request, 'crime/RIBStation/updateRequest.html', context)


def register_ribofficer(request):
    form = RibOfficerRegistrationForm()
    if request.method == 'POST':
        form = RibOfficerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='StationUser')
            user.groups.add(group)
	
            return redirect('createOfficer')
    
    context = {'form':form}
    return render(request, 'crime/RIBStation/register_ribofficer.html', context)


def register_stationName(request):
    form = StationNameRegistrationForm()
    if request.method == 'POST':
        form = StationNameRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='RIBStation')
            user.groups.add(group)
			
            messages.success(request, 'A user has been successfully registered')
            
            return redirect('createRIBStation')
    
    context = {'form':form}
    return render(request, 'crime/RIBHQ/register_StationName.html', context)

@unauthenticated_user
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get()
            return redirect('loginOrg.html')
    context = {'form':form}
    return render(request,'crime/RIBStation/register.html', context)

@unauthenticated_user
def index(request):
	
	context = {}
	messages.success(request, 'Welcome To SCSEA System')
	return render(request, 'crime/index.html', context)	

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the allowed user in
            user = form.get_user()
            login(request, user)
            if RIBHeadquarter.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home_Hq')
            elif RIBStation.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home_Station')
            elif StationUser.objects.filter(user=user):
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('home_Officer')
			       
    else:
        form = AuthenticationForm()
    return render(request, 'crime/loginOrg.html', { 'form': form })



def logoutUser(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def homeHq(request):
	today = datetime.datetime.now()
	cases = Case.objects.all()
	officers = Officer.objects.all()
	stations = RIBStation.objects.all()
	suspects = Suspect.objects.all()
	total_suspects = suspects.count()
	total_cases = cases.count()
	finished = cases.filter(status='Finished').count()
	pending = cases.filter(status='Pending').count()
	studied = cases.filter(status='Studied').count()

	cases_remera = Case.objects.filter(ribstation = 1).count()
	cases_kicukiro = Case.objects.filter(ribstation = 2).count()
	cases_rwezamenyo = Case.objects.filter(ribstation = 3).count()
	cases_muhanga = Case.objects.filter(ribstation = 7).count()
	cases_nyagatare = Case.objects.filter(ribstation = 6).count()
	cases_gatuna = Case.objects.filter(ribstation = 8).count()
	cases_ruli = Case.objects.filter(ribstation = 5).count()


	year = datetime.datetime.now().year

	january = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=1).count()
	february = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=2).count()
	march = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=3).count()
	april = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=4).count()
	may = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=5).count()
	june = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=6).count()
	july = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=7).count()
	august = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=8).count()
	september = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=9).count()
	october = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=10).count()
	november = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=11).count()
	december = Suspect.objects.filter(date_arrested__year__gte=year, date_arrested__month=12).count()

	robbery_cases = Case.objects.filter(crimeType = 'Robbery').count()
	violent_cases = Case.objects.filter(crimeType = 'Violent').count()
	murder_cases = Case.objects.filter(crimeType = 'Murder').count()

	context = {'cases':cases, 'suspects':suspects,'stations':stations,'today':today,
	'total_casess':total_cases,'finished':finished,'officers':officers,'studied':studied,
	'pending':pending, 'cases_remera':cases_remera,'cases_kicukiro':cases_kicukiro, 
	'cases_rwezamenyo': cases_rwezamenyo,'cases_muhanga': cases_muhanga,'cases_nyagatare': cases_nyagatare, 'cases_gatuna':cases_gatuna,'cases_ruli':cases_ruli,
	'january':january, 'february':february, 'march': march,
	'april': april, 'may': may, 'june': june, 'july': july, 'august': august, 'september':september, 
	'october': october, 'november': november, 'december': december,
	'robbery_cases':robbery_cases, 'violent_cases':violent_cases, 'murder_cases':murder_cases
	  }
	messages.success(request, 'Logged In as RIB Headquater User')
	return render(request, 'crime/RIBHQ/DashboardHq.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def homeStation(request):
	today = datetime.datetime.now()
	user = request.user
	ribstation = RIBStation.objects.get(user=user)
	cases = Case.objects.filter(ribstation=ribstation).order_by('-date_reported')

	paginator = Paginator(cases, 5)
	
	page_number = request.GET.get('page')
	
	page_obj = paginator.get_page(page_number)

	suspects = Suspect.objects.filter(ribstation=ribstation)
	total_suspects = suspects.count()
	total_cases = cases.count()
	finished = cases.filter(status='Finished').count()
	pending = cases.filter(status='Pending').count()
	studied = cases.filter(status='Studied').count()

	context = {'cases':cases, 'suspects':suspects,'today':today,
    'total_casess':total_cases,'finished':finished,'studied':studied,
    'pending':pending, 'page_obj':page_obj }
	messages.success(request, 'Logged In as RIBStation User')
	return render(request, 'crime/RIBStation/DashboardStation.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def homeOfficer(request):
	today = datetime.datetime.now()
	user = request.user
	stationuser = StationUser.objects.get(user=user)
	cases = Case.objects.filter(stationuser=stationuser).order_by('-date_reported')
	
	suspects = Suspect.objects.filter(stationuser=stationuser)
	total_suspects = suspects.count()
	total_cases = cases.count()
	finished = cases.filter(status='Finished').count()
	pending = cases.filter(status='Pending').count()
	studied = cases.filter(status='Studied').count()
	
	paginator = Paginator(cases, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	context = {'cases':cases, 'suspects':suspects,
    'total_casess':total_cases,'finished':finished,'today':today,
    'pending':pending,'studied':studied , 'page_obj':page_obj}
	messages.success(request, 'Logged In as Station Officer')
	return render(request, 'crime/StationOfficer/DashboardOfficer.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def crimeSuspect(request):
	user = request.user
	stationuser = StationUser.objects.get(user=user)
	
	cases = Case.objects.filter(stationuser=stationuser)
	
	suspects = Suspect.objects.filter(stationuser=stationuser)
	total_suspects = suspects.count()
	total_cases = cases.count()
	finished = cases.filter(status='Finished').count()
	pending = cases.filter(status='Pending').count()
	studied = cases.filter(status='Studied').count()
	context = {'cases':cases, 'suspects':suspects,
    'total_suspects':total_suspects,'finished':finished,
    'pending':pending,'studied':studied }
	return render(request, 'crime/StationOfficer/case_suspect.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createRIBStation(request):
	form = RibstationForm()
	if request.method == 'POST':
		form = RibstationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'RIBStation has been created Successfully')
			return redirect('createRIBCommander')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/ribstation_Form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def RIBstationList(request):
    stations = RIBStation.objects.all()
    return render(request, 'crime/RIBHQ/RIBstationList.html', {'stations':stations})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createStationName(request):
	form = RibstationForm()
	if request.method == 'POST':
		form = RibstationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Station has been Created Successfully')
			return redirect('home_HQ')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/officer_form.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createRIBCommander(request):
	form = RibCommanderForm()
	if request.method == 'POST':
		form = RibCommanderForm(request.POST)
		if form.is_valid():
			form.save()
			# messages.success(request, 'RIB Commander has been created Successfully')
			return redirect('RIBstationList')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/ribcommander_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def createOfficer(request):
	user = request.user
	ribstation = RIBStation.objects.get(user=user)
	form = StationUserForm()
	if request.method == 'POST':
		form = StationUserForm(request.POST)
		if form.is_valid():
			stationUser = form.save(commit=False)
			stationUser.ribstation = ribstation  # Assign the ribstation of the logged-in user
			stationUser.save()
			messages.success(request, 'RIB Officer has been created Successfully')
			return redirect('officerList')

	context = {'form':form}
	return render(request, 'crime/RIBStation/officer_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def officerList(request):
	user = request.user
	ribstation = RIBStation.objects.get(user=user)

	officers = StationUser.objects.filter(ribstation=ribstation)
	return render(request, 'crime/RIBStation/officerList.html', {'officers':officers})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def officerListHQ(request):
	# user = request.user
	# ribstation = RIBStation.objects.get(user=user)

	officers = StationUser.objects.all()
	return render(request, 'crime/RIBHQ/Caseofficers.html', {'officers':officers})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def caseList(request):
	user = request.user
	ribstation = RIBStation.objects.get(user=user)
	cases = Case.objects.filter(ribstation=ribstation)
	return render(request, 'crime/RIBStation/caseList.html', {'cases':cases})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def evidenceList(request):
	suspect = Suspect.objects.all()
	evidences = Evidence.objects.all()
	return render(request, 'crime/StationOfficer/evidenceList.html', {'suspect':suspect, 'evidences':evidences})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])	
def witnes(request, pk_susp):
    suspect = Suspect.objects.get(id=pk_susp)
    reporters = suspect.reporters.all()
    reporter_count = reporters.count()
    context = {'suspect':suspect,'reporters':reporters,'reporter_count':reporter_count}
    return render(request, 'crime/StationOfficer/witness.html',context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def suspect(request, pk_susp):
    suspect = Suspect.objects.get(id=pk_susp)
    evidences = suspect.evidences.all()
    evidence_count = evidences.count()
    context = {'suspect':suspect,'evidences':evidences,'evidence_count':evidence_count}
    return render(request, 'crime/StationOfficer/suspect.html',context)
@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def view(request, pk_susp):
    suspect = Suspect.objects.get(id=pk_susp)
    evidences = suspect.evidences.all()
    evidence_count = evidences.count()
    context = {'suspect':suspect,'evidences':evidences,'evidence_count':evidence_count}
    return render(request, 'crime/StationOfficer/view.html',context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def suspectList(request):
    suspect = Suspect.objects.all()
    return render(request, 'crime/StationOfficer/suspectList.html', {'suspect':suspect})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def criminalRecord(request):
	suspects = Suspect.objects.all()
	myFilter = SuspectFilter(request.GET, queryset=suspects)
	suspects = myFilter.qs 
	context = {'suspects':suspects,
	'myFilter':myFilter}
	return render(request, 'crime/RIBHQ/criminalRecordList.html', context)
    

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])

def createCase(request):
    user = request.user
    ribstation = RIBStation.objects.get(user=user)  # Get the logged-in user's RIBStation
    form = CaseForm()

    if request.method == 'POST':
        form = CaseForm(request.POST)
        
        # Filter stationuser to only include those associated with the same ribstation
        form.fields['stationuser'].queryset = StationUser.objects.filter(ribstation=ribstation)

        if form.is_valid():
            case = form.save(commit=False)
            case.ribstation = ribstation  # Assign the current ribstation to the case
            case.status = 'Pending'
            case.save()

            # Sending the SMS to the reporter
            reporterPhoneNumber = request.POST['reporter_phone']
            reporterName = request.POST['reporter_name']
            caseName = request.POST['case_name']
            ribName = request.POST['victim_address']

            send_sms_to_reporter(reporterPhoneNumber, reporterName, caseName, ribName)
            messages.success(request, 'Case has been Initiated Successfully and Reporter has been Notified')
            return redirect('caseList')
			 # Send an email to the reporter
            subject = f"Case {case.case_number} has been Initiated"
            message = f"Dear {reporterName},\n\nYour case '{caseName}' has been successfully initiated with case number {case.case_number}. We will keep you updated on the progress.\n\nRegards,\nRIBStation"
            from_email = settings.DEFAULT_FROM_EMAIL  # Make sure DEFAULT_FROM_EMAIL is configured in settings.py

            send_mail(subject, message, from_email, [reporterEmail])
            messages.success(request, 'Case has been Initiated Successfully and Reporter has been Notified')
            return redirect('caseList')


    # Make sure the stationuser queryset is set for the GET request as well
    form.fields['stationuser'].queryset = StationUser.objects.filter(ribstation=ribstation)

    context = {'form': form}
    return render(request, 'crime/RIBStation/case_form.html', context)

"""
	Method to send an sms to the reporter that his/her case was successfully received.
"""
def send_sms_to_reporter(receiver, name, caseName, ribName):
    message = f'Dear,' + name + \
        ' The case you have reported which has Re_ No:' + caseName + ' Has been received and the investigation is in process , From ' + ribName + ' Station  Thank you '
    Suspect.send_sms(receiver, message)

def send_sms_to_close(receiver, name, caseName, ribName):
    message = f'Dear,' + name + \
        ' The case you have reporter which have No:' + caseName + ' Has been Closed and the investigation is Closed , From ' + ribName + ' Station  Thank you '
    Suspect.send_sms(receiver, message)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def updateCase(request, pk):

	case = Case.objects.get(id=pk)
	form = CaseForm(instance=case)

	if request.method == 'POST':
		form = CaseForm(request.POST, instance=case)
		if form.is_valid():
			form.save()
			messages.success(request, 'Case has been Updated Successfully')
			return redirect('caseList')

	context = {'form':form}
	return render(request, 'crime/RIBStation/case_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def deleteCase(request, pk):
	case = Case.objects.get(id=pk)
	if request.method == "POST":
		case.delete()
		return redirect('home_Station')

	context = {'item':case}
	return render(request, 'crime/RIBStation/deleteCase.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def createSuspect(request, case_pk):
	user = request.user
	case = Case.objects.get(id=case_pk) 
	stationuser = StationUser.objects.get(user=user)

	form = SuspectForm()
	if request.method == 'POST':
		form = SuspectForm(request.POST)
		if form.is_valid():
			suspect = form.save(commit=False)
			suspect.ribstation = stationuser.ribstation  # Assign the ribstation of the logged-in user

			suspect.stationuser = stationuser
			case.status = 'Studied'
			case.save()
			suspect.save()
			case.suspects.add(suspect)
			messages.success(request, 'Suspect has been Linked to The case Successfully')
			return redirect('crimeSuspect')

	context = {'form':form, 'case':case}
	return render(request, 'crime/StationOfficer/suspect_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def viewCaseSuspects(request, case_pk):

	case = Case.objects.get(id=case_pk)
	suspects = case.suspects.all()

	context = {'suspects':suspects, 'case':case}
	return render(request, 'crime/StationOfficer/caseSuspects.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def updateSuspect(request, case_pk):

	suspect = Suspect.objects.get(id=case_pk)
	form = SuspectForm(instance=suspect)

	if request.method == 'POST':
		form = SuspectForm(request.POST, instance=suspect)
		if form.is_valid():
			form.save()
			return redirect('suspectList')

	context = {'form':form}
	return render(request, 'crime/StationOfficer/suspect_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def deleteSuspect(request, case_pk):
	suspect = Suspect.objects.get(id=case_pk)
	if request.method == "POST":
		suspect.delete()
		return redirect('suspectList')

	context = {'item':suspect}
	return render(request, 'crime/StationOfficer/deleteSuspect.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def createEvidence(request, suspect_pk):
	# variable to store current evidence value.
	current_evidence_rate = Suspect.objects.filter(id=suspect_pk).values_list('evidence_rate',flat=True)[0]
	# Number of evidences for a suspect.

	suspect_evidences_length = Suspect.objects.filter(id=suspect_pk).values_list("evidences", flat=True).count()

	print(" sel "+str(suspect_evidences_length))
	print(" current ev "+str(current_evidence_rate))

	sel = 0
	if current_evidence_rate == 0.0:
		sel = 1
	elif suspect_evidences_length == 1 :
		sel = suspect_evidences_length + 1
	else: 
		sel = suspect_evidences_length + 1
	"""
	calculate the rate of evidence according to the evidence. 
	"""
	print("length is "+ str(suspect_evidences_length))
	rate_for_easy = (current_evidence_rate + 20 ) / sel
	rate_for_medium = (current_evidence_rate + 30 ) / sel
	rate_for_Difficult = (current_evidence_rate + 50 ) / sel 


	suspect = Suspect.objects.get(id=suspect_pk)

	form = EvidenceForm()
	if request.method == 'POST':
	
		form = EvidenceForm(request.POST, request.FILES)
		if form.is_valid():
			# print(str(form.cleaned_data['level']))
			if str(form.cleaned_data['level'])  == 'Easy' :
				Suspect.objects.filter(id=suspect_pk).update(evidence_rate=rate_for_easy)
			if str(form.cleaned_data['level'])  == 'Middle' :
				Suspect.objects.filter(id=suspect_pk).update(evidence_rate=rate_for_medium)
			if str(form.cleaned_data['level'])  == 'Difficult' :
				Suspect.objects.filter(id=suspect_pk).update(evidence_rate=rate_for_Difficult)

			evidence = form.save()
			suspect.evidences.add(evidence)

			messages.success(request, 'Evidence has been Linked Successfully')
			return redirect('crimeSuspect')


	context = {'form':form, 'suspect':suspect}
	return render(request, 'crime/StationOfficer/evidence_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])

def find_primary_suspects(request, suspect_pk):
	
	"""
	implement calculation to add status of primary suspect after 
	"""
	suspects_rate = Suspect.objects.filter(id=suspect_pk).values_list('crime_rate',flat=True)[0]
	evidences_rate = Suspect.objects.filter(id=suspect_pk).values_list('evidence_rate',flat=True)[0]
	witness_rate = Suspect.objects.filter(id=suspect_pk).values_list('witness_rate',flat=True)[0]


	print('suspect rate is' + str(suspects_rate))
	print('evidence rate is' + str(evidences_rate))
	print('witness rate is' + str(witness_rate))

	"""
	calculate the total of evidences rate over 50 plus the 
	rate of suspect answers rate over 50 plus evidence rate over
	"""
	total_rate_over = (suspects_rate + evidences_rate + witness_rate) / 150
	total_rate = total_rate_over * 100
	print('the total is '+ str(total_rate))
	
	suspect_for_update = Suspect.objects.get(id=suspect_pk)

	if total_rate >= 50:
		# implement changing status to primary suspect here
		print("primary suspect")
		# suspect_for_update.update(suspect_status='primary_suspect')
		suspect_for_update.suspect_status = 'primary_suspect'
  
  		#suspect release date update
		today = datetime.datetime.now()  
		suspect_for_update.date_released = today
		suspect_for_update.save()
	elif total_rate >=25 and total_rate < 50 :
		#implement status middle status continue investigation
		print("Continue investigation to suspect")
		suspect_for_update.suspect_status = 'middleFromCase'
  
  		#suspect release date update
		today = datetime.datetime.now()  
		suspect_for_update.date_released = today
		suspect_for_update.save()
	else:
		# implement Free
		suspect_for_update.suspect_status = 'freeFromCase'
  
		#suspect release date update
		today = datetime.datetime.now()  
		suspect_for_update.date_released = today
		suspect_for_update.save()

  
		# case status update
	suspect = Suspect.objects.get(id=suspect_pk)
	case = suspect.case_set.first()
	case.status ='Finished'
	case.save()


	messages.success(request, 'Suspect Decision Analysed and Generated successfully')
	context = {'suspect':Suspect.objects.get(id=suspect_pk), 'case':case, 'evidences':Suspect.objects.get(id=suspect_pk).evidences.all(),'evidence_count':Suspect.objects.get(id=suspect_pk).evidences.all().count()}
	return render(request, 'crime/StationOfficer/suspectDecisionReport.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def updateEvidence(request, pk):

	evidence = Evidence.objects.get(id=pk)
	form = EvidenceForm(instance=evidence)

	if request.method == 'POST':
		form = EvidenceForm(request.POST, instance=evidence)
		if form.is_valid():
			form.save()
			return redirect('evidence')

	context = {'form':form}
	return render(request, 'crime/StationOfficer/evidence_Form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def createReporter(request, suspect_pk):
	suspect = Suspect.objects.get(id=suspect_pk)
	form = ReporterForm()
	if request.method == 'POST':
		form = ReporterForm(request.POST)
		if form.is_valid():
			reporter = form.save()
			suspect.reporters.add(reporter)
			messages.success(request, 'Witness has been Linked Successfully')
			return redirect('crimeSuspect')

	context = {'form':form, 'suspect':suspect}
	return render(request, 'crime/StationOfficer/reporter_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def reporterList(request):
    reporter = Reporter.objects.all()
    return render(request, 'crime/StationOfficer/reportertList.html', {'reporter':reporter})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createQuestionForSuspect(request):
	form = QuestionForm()
	if request.method == 'POST':
		form = QuestionForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Question has been Posted Successfully')
			return redirect('QuestionSuspList')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/question_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createQuestionForReporter(request):
	form = QuestionRepoForm()
	if request.method == 'POST':
		form = QuestionRepoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('QuestionRepoList')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/questionForReporter.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def QuestionSuspList(request):
    questions = QuestionSuspect.objects.all()
    return render(request, 'crime/RIBHQ/questionList.html', {'questions':questions})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def QuestionRepoList(request):
    questions = QuestionReporter.objects.all()
    return render(request, 'crime/RIBHQ/questionRepoList.html', {'questions':questions})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createAnswer(request):
	form = AnswerForm()
	if request.method == 'POST':
		form = AnswerForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Answer has been Posted Successfully')
			return redirect('AnswerList')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/answer_form.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def AnswerList(request):
    answers = Answer.objects.all()
    return render(request, 'crime/RIBHQ/answerList.html', {'answers':answers})


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def createCAQS(request, pk_suspect, crimeType):
    user = request.user
    stationuser = StationUser.objects.get(user=user)

    # Get all questions related to this crime type
    questions = QuestionSuspect.objects.all()
    
    # Define the formset for the `CAQS` model
    QuestionFormSet = inlineformset_factory(Suspect, CAQS, fields=('question', 'answer'), extra=questions.count())
    
    # Retrieve the suspect
    suspect = Suspect.objects.get(id=pk_suspect)
    
    # Create the formset instance
    formset = QuestionFormSet(queryset=CAQS.objects.filter(question__crimeType=crimeType), instance=suspect)
    
    if request.method == 'POST':
        formset = QuestionFormSet(request.POST, instance=suspect)

        if formset.is_valid():
            count = 0
            not_applied = 0
            
            # Iterate through the formset and process the forms
            for form in formset:
                # Access the individual form's cleaned data
                answer = form.cleaned_data.get('answer')
                
                # Calculate the count and not_applied values
                if str(answer) == "yes":
                    count += 1
                elif str(answer) == "not_applied":
                    not_applied += 1
                
                # Access the CAQS instance behind the form and assign ribstation and stationuser
                caqs_instance = form.save(commit=False)
                caqs_instance.ribstation = stationuser.ribstation  # Assign the ribstation of the logged-in user
                caqs_instance.stationuser = stationuser  # Assign the stationuser of the logged-in user
                caqs_instance.save()  # Save the form instance

            # Calculate the total number of applicable questions (excluding "not_applied")
            questionsTotal = questions.count() - not_applied

            # Calculate the rate based on "yes" answers, and return the rate out of 50
            rate = 50 * float(count) / float(questionsTotal) if questionsTotal > 0 else 0
            Suspect.objects.filter(id=pk_suspect).update(crime_rate=rate)

            # Update the suspect status to "asked"
            suspect.suspect_status = "asked"
            suspect.save()  # Save the updated suspect instance

            messages.success(request, 'Questions have been Linked to Suspect Successfully')
            return redirect('CAQSList')

    context = {'form': formset, 'suspect': suspect}
    return render(request, 'crime/StationOfficer/cransquestsusp_Form.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def CAQSList(request):
    user = request.user
    rib_user = StationUser.objects.get(user=user)
    
    # If you want to filter by a specific suspect
    suspect_id = request.GET.get('suspect_id')  # Assuming the suspect ID is passed as a query parameter
    if suspect_id:
        # Filter based on both stationuser and suspect
        quesans = CAQS.objects.filter(stationuser=rib_user, suspect__id=suspect_id)
    else:
        # If no suspect is provided, just filter by the stationuser
        quesans = CAQS.objects.filter(stationuser=rib_user)

    return render(request, 'crime/StationOfficer/questAnsList.html', {'quesans': quesans})



@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def createCAQW(request, pk_witness):
	suspect = Suspect.objects.filter(reporters__id=pk_witness)
	questions = QuestionReporter.objects.all()
	QuestionFormSet = inlineformset_factory(Reporter, CAQW, fields=('question', 'answer'), extra=questions.count())
	reporter = Reporter.objects.get(id=pk_witness)
	formset = QuestionFormSet(queryset=CAQW.objects.none(),instance=reporter)
	if request.method == 'POST':
		formset = QuestionFormSet(request.POST,instance=reporter)

		if formset.is_valid():
			count=0
			for form in formset:
				if str(form.cleaned_data['answer']) == "yes":
					count+=1
					form.save()

			"""
			  calculate the rate over 50 of from suspect answers
			  find the average based on lenght of questions.
			  and return the rate of Yes ones. means total marks will be
			  calculated out of 50.
			"""
			rate = 50 * float(count)/float(questions.count())
			suspect.update(witness_rate=rate)



			
			messages.success(request, 'Qeustions has been Linked to Witness Successfully')
			return redirect('crimeSuspect')


	context = {'form':formset, 'reporter':reporter}
	return render(request, 'crime/StationOfficer/cransquestWitness_Form.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def createCrime(request):
	form = CrimeForm()
	if request.method == 'POST':
		form = CrimeForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Crime has been Created Successfully')
			return redirect('CrimeList')

	context = {'form':form}
	return render(request, 'crime/RIBHQ/crime_form.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def CrimeList(request):
    crimes = Crime.objects.all()
    return render(request, 'crime/RIBHQ/crimeList.html', {'crimes':crimes})

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def generalStatisticalReport(request):
    n_suspects = 0
    user = request.user
    cases = Case.objects.all()
    officers = Officer.objects.all()
    stations = RIBStation.objects.all()
    suspects = Suspect.objects.all()
    reporters = Reporter.objects.all()
 
    context = {'stations':stations,'cases':cases,'suspects':suspects,'officers':officers,'reporters':reporters}
    return render(request, 'crime/RIBHQ/GeneralReport.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def casesAnalyse(request):
	user = request.user
	stationuser = StationUser.objects.get(user=user)	
	cases = Case.objects.filter(stationuser=stationuser, status='Finished')	
	suspects = Suspect.objects.filter(stationuser=stationuser)
	
	context = {'cases':cases, 'suspects':suspects}
	
	return render(request, 'crime/StationOfficer/caselistAnalysis.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def stationClosedCases(request):
	user = request.user
	rib_station = RIBStation.objects.get(user=user)
	cases = Case.objects.filter(ribstation=rib_station, status='Finished')
	suspects = Suspect.objects.filter(ribstation=rib_station)
	
	context = {'cases':cases, 'suspects':suspects,'rib_station':rib_station}
	
	return render(request, 'crime/RIBStation/casesClosed.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def CanceledCases(request):
	rib_station = RIBStation.objects.all()
	cases = Case.objects.filter(status='Finished')
	# suspects = Suspect.objects.filter(ribstation=rib_station)
	# 'suspects':suspects,
	context = {'cases':cases, 'rib_station':rib_station}
	
	return render(request, 'crime/RIBHQ/canceledCase.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def analyseCaseSuspects(request, case_pk):

	case = Case.objects.get(id=case_pk)
	suspects = case.suspects.all()

	context = {'suspects':suspects, 'case':case}
	return render(request, 'crime/StationOfficer/caseSuspectsAnalysis.html', context)

@login_required(login_url='login_view')
# @allowed_users(allowed_roles=['RIBStation'])
def ClosedCaseSuspects(request, case_pk):

	caseSuspects = Case.objects.get(id=case_pk)
	suspects = caseSuspects.suspects.all()
	officer = caseSuspects.stationuser
	context = {'suspects':suspects,'officer':officer, 'caseSuspects':caseSuspects}
	return render(request, 'crime/RIBStation/SuspectsForClosedcase.html', context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def RIBClosedCaseSuspects(request, case_pk):

	caseSuspects = Case.objects.get(id=case_pk)
	suspects = caseSuspects.suspects.all()
	officer = caseSuspects.stationuser
	context = {'suspects':suspects,'officer':officer, 'caseSuspects':caseSuspects}
	return render(request, 'crime/RIBHQ/RIBSuspectsForClosedcase.html', context)

def some_view(request):
	suspect = Suspect.objects.all()
	buffer = io.BytesIO()
	p = canvas.Canvas(buffer)
	p.drawString(100, 100, "This is the Evidence of Suspect,.")
	p.showPage()
	p.save()
	buffer.seek(0)
	return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
	
#=========================================
#A SECTION OF ALL REPORTS IMPLEMENTATION
#========================================

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def printSuspectsHQ(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printSuspectsHQ.html')

	suspects = Suspect.objects.all()

	context = {'suspects':suspects,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printSuspectsHQ.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Suspests List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def printRIBStationHQ(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printRIBStationHQ.html')

	ribstations = RIBStation.objects.all()

	context = {'ribstations':ribstations,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printRIBStationHQ.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "RIBStation List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def printOfficerHQ(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printOfficersHQ.html')

	officers = Officer.objects.all()

	context = {'officers':officers,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printOfficersHQ.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "RIBOfficers List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def printCasaesHQ(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printcasesHQ.html')

	cases = Case.objects.all()

	context = {'cases':cases,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printcasesHQ.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "All Cases List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def printWitnessHQ(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printwitnessHQ.html')

	repoters = Reporter.objects.all()

	context = {'repoters':repoters,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printwitnessHQ.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Witnesses List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def printEvidence(request):
	user = request.user
	rib_user = StationUser.objects.get(user=user)

	suspect = Suspect.objects.filter()
	template = get_template('crime/Reports/printEvidence.html')

	evidences = suspect.evidences.all()

	context = {'suspect':suspect, 'evidences':evidences,'user':user,'rib_user':rib_user}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printEvidence.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Evidence of Suspect"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def ribStationReport(request):

	rib_stations = RIBStation.objects.all()
	cases = Case.objects.all()
	station_user = StationUser.objects.all()
	male= Officer.objects.filter(gender='M').count()
	female= Officer.objects.filter(gender='F').count()
	InspectorOfPolice = Officer.objects.filter(rank = 'InspectorOfPolice').count()
	AssistantSuperintendentofPolice = Officer.objects.filter(rank = 'AssistantSuperintendentofPolice').count()
	AssistantInspectorOfPolice = Officer.objects.filter(rank = 'AssistantInspectorOfPolice').count()


	context = {'cases':cases,'InspectorOfPolice':InspectorOfPolice,'AssistantSuperintendentofPolice':AssistantSuperintendentofPolice,
            'AssistantInspectorOfPolice':AssistantInspectorOfPolice,'rib_stations':rib_stations, 'cases':cases, 'station_user':station_user,
	'male':male, 'female':female}
	return render(request, 'crime/Reports/RIBStationReport.html',context)


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def caseReportFromRibstation(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printCasePerStation.html')

	try:
		station = request.GET.get('station')
		case = request.GET.get('case')
		officer = request.GET.get('officer')

	except:
		station = None
		case = None
		officer = None
	if station:
		if case:
			if officer:
				cases = Case.objects.filter(ribstation=station, id=case, stationuser=officer)
				
	

	context = {'cases':cases,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printCasePerStation.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Case List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def ribSuspectReport(request):

	rib_stations = RIBStation.objects.all()
	cases = Case.objects.all()
	suspects = Suspect.objects.all()
	context = {'rib_stations':rib_stations, 'cases':cases, 'suspects':suspects}
	return render(request, 'crime/Reports/RIBStationReport.html',context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def suspectReportFromCase(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printSuspectPerCase.html')

	try:
		station = request.GET.get('station')
		case = request.GET.get('case')		

	except:
		station = None
		case = None
		
	if station:
		if case:
				# case = Case.objects.filter(ribstation=station, id=case)
				case = Case.objects.get(id=case, ribstation=station)
				suspects = case.suspects.all()
			

	context = {'suspects':suspects,'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printSuspectPerCase.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Suspect List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"



@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def ribCompareReport(request):
	

	rib_stations = RIBStation.objects.all()
	case = Case.objects.all()
	cases = Case.objects.all().count()
	

	context = {'rib_stations':rib_stations, 'cases':cases, 'suspects':suspects, 'evidences':evidences, 'witness':witness}
	return render(request, 'crime/Reports/RIBStationReport.html',context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def compareTwoRibstation(request):
	user = request.user
	rib_hq = RIBHeadquarter.objects.get(user=user)
	ribLocation = rib_hq.province
	template = get_template('crime/Reports/printCompareRIBstation.html')

	evidences_station1=0
	evidences_station2=0
	witness_station1=0
	witness_station2=0
	
	try:
		station1 = request.GET.get('station1')
		station2 = request.GET.get('station2')
		crimetype = request.GET.get('crimetype')
	except:
		station1 = None
		station2 = None
		crimetype = None
		
	if station1:
		if station2:
			if crimetype:
				suspects = Suspect.objects.all()
				ribstation1 = RIBStation.objects.get(id=station1)
				station1_name = ribstation1.station_name
				
				cases_station1 = Case.objects.filter(ribstation=ribstation1, crimeType=crimetype).count()
				if cases_station1 == 0:
					suspects_station1 = 0
					if suspects_station1 == 0:
						evidences_station1 = 0
						witness_station1 = 0
					
				ribstation2 = RIBStation.objects.get(id=station2)
				station2_name = ribstation2.station_name
				
				cases_station2 = Case.objects.filter(ribstation=ribstation2, crimeType=crimetype).count()
				if cases_station2 == 0:
					suspects_station2 = 0
					if suspects_station2 == 0:
						evidence_station2 = 0
						witness_station2 = 0
					
				cases_suspects1 = Case.objects.filter(ribstation=ribstation1, crimeType=crimetype)
				cases_suspects2 = Case.objects.filter(ribstation=ribstation2, crimeType=crimetype)
				
				
				
				for case1 in cases_suspects1:
					suspects_station1 = case1.suspects.all().count()
					suspects_s1 = case1.suspects.all()

					for suspect in suspects_s1:
						evidences = suspect.evidences.all().count()
						evidences_station1 = evidences_station1 + evidences
						reporters = suspect.reporters.all().count()
						witness_station1 = witness_station1 + reporters
				
				for case2 in cases_suspects2:
					suspects_station2 = case2.suspects.all().count()
					suspects_s2 = case2.suspects.all()

					for suspect in suspects_s2:
						evidences = suspect.evidences.all().count()
						evidences_station2 = evidences_station2 + evidences
						reporters = suspect.reporters.all().count()
						witness_station2 = witness_station2 + reporters
						

	context = {'crimetype':crimetype, 'cases_station1':cases_station1, 'cases_station2': cases_station2,
	 		  'station1_name':station1_name, 'station2_name':station2_name, 
			   'suspects_station1':suspects_station1, 'suspects_station2':suspects_station2,
			  'evidences_station1':evidences_station1,'evidences_station2':evidences_station2,
			  'witness_station1':witness_station1,'witness_station2':witness_station2,
			  'user':user,'rib_hq':rib_hq,'ribLocation':ribLocation
			   }
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printCompareRIBstation.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Case List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBHeadquarter'])
def printCaseInfo(request):
	template = get_template('crime/Reports/printCaseStation.html')

	cases = Case.objects.all()

	context = {'cases':cases}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printCaseStation.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "All Cases List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"



@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def stationStatReporting(request):

	user = request.user
	rib_station = RIBStation.objects.get(user=user)
	cases = Case.objects.filter(ribstation=rib_station)

	male= StationUser.objects.filter(ribstation=rib_station, gender='M').count()
	female= StationUser.objects.filter(ribstation=rib_station, gender='F').count()
	Civilian = StationUser.objects.filter(ribstation=rib_station, rank = 'Civilian').count()
	Corporal = StationUser.objects.filter(ribstation=rib_station, rank = 'Corporal').count()
	Sergeant = StationUser.objects.filter(ribstation=rib_station, rank = 'Sergeant').count()


	context = {'cases':cases,'Civilian':Civilian,'Corporal':Corporal,'Sergeant':Sergeant,
	'male':male, 'female':female}
	return render(request, 'crime/Reports/stationReporting.html',context)




@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def StationCaseInfo(request):
	template = get_template('crime/Reports/printCaseStationInfo.html')
	user = request.user
	rib_station = RIBStation.objects.get(user=user)
	ribLocation = rib_station.province
	
	try:	
		case = request.GET.get('case')	
	except:
		
		case = None		
	
	if case:	
			case = Case.objects.filter(id=case)
			
	context = {'case':case,'user':user, 'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printCaseStationInfo.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Case Information"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def CompareCaseSuspectReport(request):

	user = request.user
	rib_station = RIBStation.objects.get(user=user)
	cases = Case.objects.filter(ribstation=rib_station)
	
	context = {'cases':cases} 
	return render(request, 'crime/Reports/RIBStationReport.html',context)



@login_required(login_url='login_view')
@allowed_users(allowed_roles=['RIBStation'])
def printSuspectsOnTwoCase(request):
	
	template = get_template('crime/Reports/printSuspectsOnTwoCase.html')
	user = request.user
	rib_station = RIBStation.objects.get(user=user)
	ribLocation = rib_station.province
	
	try:
		case1 = request.GET.get('case1')
		case2 = request.GET.get('case2')
	except:	
		case1 = None
		case2 = None

	if case1:	
		first_case = Case.objects.get(id=case1)
		nameC1 = first_case.case_number
		cases_suspects1 = first_case.suspects.all()
		if case2:
			second_case = Case.objects.get(id=case2)
			nameC2 = second_case.case_number
			cases_suspects2 = second_case.suspects.all()

	context = {'cases_suspects1':cases_suspects1, 'cases_suspects2':cases_suspects2,
				'nameC1':nameC1 ,'nameC2':nameC2, 'user':user,'ribLocation':ribLocation}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printSuspectsOnTwoCase.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Suspect List on Two Cases"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"


@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])
def presentPrimarySuspect(request):
	user = request.user
	rib_user = StationUser.objects.get(user=user)
	template = get_template('crime/Reports/printPrimarySuspect.html')

	suspects = Suspect.objects.filter(stationuser=rib_user)

	context = {'suspects':suspects,'user':user,'rib_user':rib_user}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/printPrimarySuspect.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Primary Suspests List"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"


def ajaxSearch(request):
    if 'term' in request.GET:
        qs = Suspect.objects.filter(f_name__icontains=request.GET.get('term'))
        qs = Suspect.objects.filter(f_name__istartswith=request.GET.get('term'))
        f_name = list()
        for susp in qs:
            f_name.append(susp.f_name)
        return JsonResponse(f_name, safe=False)
    context = {}
    return render(request, 'ajaxSuspectForm.html', context)

@login_required(login_url='login_view')
@allowed_users(allowed_roles=['StationUser'])

def primaryOrReleaseReport(request, pk_suspect):
	user = request.user
	template = get_template('crime/Reports/primaryOrReleaseReport.html')
	today = datetime.datetime.now()

	suspect = Suspect.objects.get(id=pk_suspect)
	case = suspect.case_set.first()
	reporters = suspect.reporters.all()
	evidences = suspect.evidences.all()

	# reporterPhoneNumber = request.POST['reporter_phone']
	# reporterName = request.POST['reporter_name']
	# caseName = request.POST['case_name']
	# ribName = request.POST['ribstation']

	# send_sms_to_close(reporterPhoneNumber,reporterName,caseName,ribName)

	context = {'user':user, 'suspect':suspect, 'case':case, 'reporters':reporters, 'evidences':evidences, 'today':today}
	html = template.render(context)
	pdf= render_to_pdf('crime/Reports/primaryOrReleaseReport.html', context)
	if pdf:
		response = HttpResponse(pdf, content_type='application/pdf')
		file_name = "Primary or Release Suspect Report"
		content = "inline; filename='%s'" %(file_name)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(file_name)
		response['Content-Disposition'] = content
		return response
		return HttpResponse*"Not found"









	