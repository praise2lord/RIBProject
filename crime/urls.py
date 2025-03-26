# from django.conf  import settings
# from django.conf.urls.static import static
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                         document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from crime.views import login
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name="index"),
    path('login_view/', views.login_view, name="login_view"),
    path('registerPage/', views.registerPage, name="registerPage"),
    path('register_ribofficer/', views.register_ribofficer, name="register_ribofficer"),
    path('register_stationName/', views.register_stationName, name="register_stationName"),
    path('logout',views.logoutUser, name='logout'),
    path('error401', views.error401, name='error401'),
    path('errorDelete', views.errorDelete, name='errorDelete'),
    path('errorUpdateCase', views.errorUpdateCase, name='errorUpdateCase'),
    path('errorDeleteCase/<str:case_pk>/', views.errorDeleteCase, name='errorDeleteCase'),
    path('home_Hq/', views.homeHq, name="home_Hq"),
    path('home_Station/', views.homeStation, name="home_Station"),
    path('home_Officer/', views.homeOfficer, name="home_Officer"),
    path('createStationName/', views.createStationName, name="createStationName"),
    path('createRIBStation/', views.createRIBStation, name="createRIBStation"),
    path('createRIBCommander/', views.createRIBCommander, name="createRIBCommander"),
    path('createOfficer/', views.createOfficer, name="createOfficer"),
    path('officerList/', views.officerList, name="officerList"),
    path('officerListHQ/', views.officerListHQ, name="officerListHQ"),
    path('CanceledCases/', views.CanceledCases, name="CanceledCases"),
    path('RIBstationList/', views.RIBstationList, name="RIBstationList"),
    path('suspect/<str:pk_susp>/', views.suspect, name="suspect"),
    path('view/<str:pk_susp>/', views.view, name="view"),
    
    path('witnes/<str:pk_susp>/', views.witnes, name="witnes"),
    path('caseList/', views.caseList, name="caseList"),
    path('evidence/', views.evidenceList, name="evidence"),
    path('create_case/', views.createCase, name="create_case"),
    path('update_case/<str:pk>/', views.updateCase, name="update_case"),
    path('delete_case/<str:pk>/', views.deleteCase, name="delete_case"),
    path('create_suspect/<str:case_pk>/', views.createSuspect, name="create_suspect"),
    path('suspectList/', views.suspectList, name="suspectList"),
    path('criminalRecord/', views.criminalRecord, name="criminalRecord"),
    path('crimeSuspect/', views.crimeSuspect, name="crimeSuspect"),
    path('update_suspect/<str:case_pk>/', views.updateSuspect, name="update_suspect"),
    path('delete_suspect/<str:case_pk>/', views.deleteSuspect, name="delete_suspect"),
    path('create_evidence/<str:suspect_pk>/', views.createEvidence, name="create_evidence"),
    path('update_evidence/<str:pk>/', views.updateEvidence, name="update_evidence"),
    path('createReporter/<str:suspect_pk>/', views.createReporter, name="create_reporter"),
    path('reporterList/', views.reporterList, name="reporterList"),
    path('viewCaseSuspects/<str:case_pk>/', views.viewCaseSuspects, name="viewCaseSuspects"),
    path('createQuestionForSuspect/', views.createQuestionForSuspect, name="createQuestionForSuspect"),
    path('createQuestionForReporter/', views.createQuestionForReporter, name="createQuestionForReporter"),
    path('createAnswer/', views.createAnswer, name="createAnswer"),
    path('createCAQS/<str:pk_suspect>/crimeType/<str:crimeType>/', views.createCAQS, name="createCAQS"),
    path('createCAQW/<str:pk_witness>/', views.createCAQW, name="createCAQW"),
    path('CAQSList/', views.CAQSList, name="CAQSList"),
    path('createCrime/', views.createCrime, name="createCrime"),
    path('CrimeList/', views.CrimeList, name="CrimeList"),
    path('QuestionSuspList/', views.QuestionSuspList, name="QuestionSuspList"),
    path('QuestionRepoList/', views.QuestionRepoList, name="QuestionRepoList"),
    path('AnswerList/', views.AnswerList, name="AnswerList"),
    path('casesAnalyse/', views.casesAnalyse, name="casesAnalyse"),
    path('stationClosedCases/', views.stationClosedCases, name="stationClosedCases"),
    path('ClosedCaseSuspects/<str:case_pk>/', views.ClosedCaseSuspects, name="ClosedCaseSuspects"),
    path('RIBClosedCaseSuspects/<str:case_pk>/', views.RIBClosedCaseSuspects, name="RIBClosedCaseSuspects"),
    path('analyseCaseSuspects/<str:case_pk>/', views.analyseCaseSuspects, name="analyseCaseSuspects"),
    path('generalStatisticalReport/', views.generalStatisticalReport, name="generalStatisticalReport"),
    path('some_view/', views.some_view, name="some_view"),
    path('printOfficerHQ/', views.printOfficerHQ, name="printOfficerHQ"),
    path('printSuspectsHQ/', views.printSuspectsHQ, name="printSuspectsHQ"),
    path('printRIBStationHQ/', views.printRIBStationHQ, name="printRIBStationHQ"),
    path('printEvidence/', views.printEvidence, name="printEvidence"),
    path('printCasaesHQ/', views.printCasaesHQ, name="printCasaesHQ"),
    path('printWitnessHQ/', views.printWitnessHQ, name="printWitnessHQ"),
    path('ribStationReport/', views.ribStationReport, name="ribStationReport"),
    path('caseReportFromRibstation/', views.caseReportFromRibstation, name="caseReportFromRibstation"),
    path('suspectReportFromCase/', views.suspectReportFromCase, name="suspectReportFromCase"),
    path('compareTwoRibstation/', views.compareTwoRibstation, name="compareTwoRibstation"),
    path('stationStatReporting/', views.stationStatReporting, name="stationStatReporting"),
    path('printCaseInfo/', views.printCaseInfo, name="printCaseInfo"),
    path('StationCaseInfo/', views.StationCaseInfo, name="StationCaseInfo"),
    path('CompareCaseSuspectReport/', views.CompareCaseSuspectReport, name="CompareCaseSuspectReport"),
    path('printSuspectsOnTwoCase/', views.printSuspectsOnTwoCase, name="printSuspectsOnTwoCase"),
    path('presentPrimarySuspect/', views.presentPrimarySuspect, name="presentPrimarySuspect"),
    
    path('primaryOrReleaseReport/<str:pk_suspect>/', views.primaryOrReleaseReport, name='primaryOrReleaseReport'),
    path('findPrimarySuspect/<str:suspect_pk>/', views.find_primary_suspects, name='findPrimarySuspect'),
    







 ]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# Admin Title
admin.site.site_header = "SCSEA RIB ADMNINISTRATION PANEL"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome To RIB System Admin Area"