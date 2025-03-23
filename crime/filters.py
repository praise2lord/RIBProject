import django_filters
from django_filters import DateFilter,CharFilter

from .models import *

class SuspectFilter(django_filters.FilterSet):
    suspectNID = CharFilter(field_name="suspectNID", lookup_expr='icontains')
    # phone = CharFilter(field_name="phone", lookup_expr='icontains')
    # start_date = DateFilter(field_name="date_arrested", lookup_expr='gte')
    # end_date = DateFilter(field_name="date_arrested", lookup_expr='lte')    
    class Meta:
         model = Suspect
         fields = '__all__'
         exclude = ['cell','suspectimage','village','note','evidences','reporters','relation','dob','province','crime_rate','witness_rate','evidence_rate',
         'district','f_name','l_name','date_arrested','gender','l_name','father_name','mother_name','phone']
