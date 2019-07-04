from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from seffafistatistik import views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('analizcisiz_vakalar/', AnalizcisizVakalar.as_view(), name='analizcisiz_vakalar'),
    path('analizcisiz_doktorlar/', AnalizcisizDoktorlar.as_view(), name='analizcisiz_doktorlar'),
    path('aylaragorevaka/', AylaraGoreVaka.as_view(), name='aylaragorevaka'),
    path('doktortakimesleme/', DoktorTakimEsleme.as_view(), name='doktor_takim_esleme'),
    path('miydegistirme/', MiyDegistirme.as_view(), name='miy_degistirme'),
    path('doktoruretimcidegistirme/', DoktorUretimciDegistirme.as_view(), name='doktor_uretimci_degistirme'),

    
]

