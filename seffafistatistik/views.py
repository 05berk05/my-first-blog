from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.utils import timezone
from .models import Doctor, MIY, Case, Account 
import time
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class Home(ListView):
    template_name = 'seffafistatistik/home.html'

 #Analizcisi olmayan vakalar
class AnalizcisizVakalar(ListView):
    context_object_name = 'analizcisiz_vakalar'
    template_name = 'seffafistatistik/analizcisiz_vakalar.html'
    monday= timezone.now().replace(microsecond=0,hour=0,minute=0,second=0)  - timedelta(90)
    queryset = Doctor.objects.filter(signup_time__gte= monday).select_related('account').select_related('miy').select_related('miy__account').order_by('-signup_time')
    cases = Case.objects.filter(anatec=None)

#doctors çekmek gerek bir yerden nereden?
#ID'leri nereden çekiyoruz?
class AnalizcisizDoktorlar(ListView):
    context_object_name = 'analizcisiz_doktorlar'
    template_name = 'seffafistatistik/analizcisiz_doktorlar.html'
    monday= timezone.now().replace(microsecond=0,hour=0,minute=0,second=0)  - timedelta(90)
    queryset = Doctor.objects.filter(signup_time__gte= monday).select_related('account').select_related('miy').select_related('miy__account').order_by('-signup_time')
    doctors_sinem = Doctor.objects.filter(anatec=None,miy__pk=SINEM_MIY_ID)
    print (doctors_sinem)
    doctors_sinem.update(anatec=Account.objects.get(pk=ABDULLAH_ID))
        
    doctors_basak = Doctor.objects.filter(anatec=None,miy__pk=BASAK_MIY_ID)
    print (doctors_basak)
    doctors_basak.update(anatec=Account.objects.get(pk=NIMET_ID))
        
    doctors_ozlem = Doctor.objects.filter(anatec=None,miy__pk=OZLEM_MIY_ID)
    print (doctors_ozlem)
    doctors_ozlem.update(anatec=Account.objects.get(pk=ESIN_ID))
        
    doctors_deniz = Doctor.objects.filter(anatec=None,miy__pk=DENIZ_MIY_ID)
    print (doctors_deniz)
    doctors_deniz.update(anatec=Account.objects.get(pk=BERKAY_ID))
       
    doctors_ezgi = Doctor.objects.filter(anatec=None,miy__pk=EZGI_MIY_ID)
    print (doctors_ezgi)
    doctors_ezgi.update(anatec=Account.objects.get(pk=ABDULLAH_ID))
    def get_context_data(self, **kwargs):
        context = super(AnalizcisizDoktorlar, self).get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.filter(anatec=None)
        context['doctors'] = doctors
        context['doctors_sinem'] = doctors_sinem
        context['doctors_basak'] = doctors_basak
        context['doctors_ozlem'] = doctors_ozlem
        context['doctors_deniz'] = doctors_deniz
        context['doctors_ezgi'] = doctors_ezgi

        return context

#kontrol ettim 
class AylaraGoreVaka(TemplateView): #Hangi ay kaç vaka geldi, ve vaka gönderen hekimler aktif hekimler mi
    context_object_name = 'aylaragorevaka'
    template_name = 'seffafistatistik/aylaragorevaka.html'
    monday= timezone.now().replace(microsecond=0,hour=0,minute=0,second=0)  - timedelta(90)
    queryset = Doctor.objects.filter(signup_time__gte= monday).select_related('account').select_related('miy').select_related('miy__account').order_by('-signup_time')
    def get_context_data(self, **kwargs):
        context = super(AylaraGoreVaka, self).get_context_data(**kwargs)
        x= Case.objects.filter(Q(created__gte= timezone.now().replace(month=9,day=1,microsecond=0,hour=0,minute=0,second=0)) & Q(created__lte =timezone.now().replace(month=10,day=1,microsecond=0,hour=0,minute=0,second=0) ))
        toplam_x = x.count()
        toplam_y = 0
        toplam_x_onay= 0
        toplam_y_onay= 0
        toplam_y_set= set()

        for i in x:

            if(i.doctor.monthly_stats.has_key(u'10-2017')):
                if i.doctor.monthly_stats[u'10-2017'] in ['1','2','3'] :
                    toplam_y +=1
                    toplam_y_set.add(i.doctor.id)
                    if(i.onay):
                        toplam_y_onay +=1
            else:
                print (i.doctor)

        print (toplam_x)
        print (toplam_y)
        print (toplam_y_onay)
        print (len(toplam_y_set))

        print ("-----------")
        context['x'] = x
        context['toplam_x'] = toplam_x
        context['toplam_y'] = toplam_y
        context['toplam_x_onay']= toplam_x_onay
        context['toplam_y_onay']= toplam_y_onay
        context['toplam_y_set']= toplam_y_set
        return context



class MiyDegistirme(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = 'miy_degistirme'
    template_name = 'seffaf/miy_degistirme.html'
    monday= timezone.now().replace(microsecond=0,hour=0,minute=0,second=0)  - timedelta(90)
    queryset = Doctor.objects.filter(signup_time__gte= monday).select_related('account').select_related('miy').select_related('miy__account').order_by('-signup_time')

    def get_context_data(self, **kwargs):
        context = super(MiyDegistirme, self).get_context_data(**kwargs)
        context['hale']=MIY.objects.get(id=1)
        context['nuri']=MIY.objects.get(id=7)
        context['buse']=MIY.objects.get(id=45)
        doctors_list =  ["Ab Ağiz Ve Diş Sağliği","Abbas Koç","Abdullah Babalik","Abdullah Kaya","Abdulsamet Demirkol","Abdulselam Yıldız","Abdurrahman Dörtkardeş","Adem Seven","Adile Güvenç","Adnan Batu","Adnan Koçak","Agah Tümay Akgün","Agit Bilgiç","Ahmet Gürbüz","Ahmet Müftüoğlu","Ahmet Bayramoğlu","Ahmet Utku Aydın","Ahmet Danıska","Ahmet Atlı","Ahmet Kılıç","Ahmet Dükkanci","Ahmet Kemal Kocacık","Ahmet Tevfik Bilgic","Alev Solak","Ali Toncer","Ali Güner","Ali Adalı","Ali Fuat Erciyas","Ali Haydar Güler","Alim Oktay Çatkan","Ali Onur Çakmaz","Ali Rıza Altun","Ali Yüksel Çalışkan","Ali Zeki Osmanoğlu","Alkan Bilginer","Alp Arslan","Alpay Coskun","Alper Tunga Bahat","Ani Cömert","Anıl Uyanık","Arten Dyrmishi","Aslı Kale Toker","Aslıhan Gül Kalaoğlu","Aycan Beceren","Aydin Görgün","Aydin Şirinler","Ayfer Aydin Berke","Ayhan Öztürk","Ayhan Deniz","Ayni Şeref Kalpakçı","Aynur Yeni","Ayrıl Metin Cebeci","Ayşe Yılmaz","Ayşe Ertuğrul","Ayşe Bahar Açıkgözoğlu","Ayşe Banu Uluceviz","Ayşe Fatma Turan","Ayşegül Şahin","Ayşe Nesrin Güzey","Ayşenur Batu Güney","Ayşin Gülenç Cokşun","Aysun Dorman","Aysun Saka","Aysun Azim Karataç","Aziz Çalışkan","Aziz Bülent Yıldırım","Bahadir Özbay","Bahadır Odabaş","Bahar Bostan","Bahri Gürenci","Bakır Pişirici","Bayram Asarkaya","Belkıs Teke","Berna Dinçer Kırbıyık","Berna Zorkun","Berrak Erdem","Betül Karaayvaz","Beytullah Gülsoy","Buket Kılınç","Buket Özer","Bülent Toyboy","Bülent Türkücü","Bülent Akdereli","Bünyamin Çahan","Burcu Barı","Burcu Gencel","Burcu Usta Selamet","Buse Çolpan Diş","Çağatay Sözer","Çağlan Fırat Çağlar","Can Dönmez","Can Kocaman","Canan Yılmaz Ergen","Can Berk Özer","Caner Asma","Cem Özkartal","Cem Doğruyol","Cengiz Mankut","Cengiz Bahcevan","Cenk Göçer","Cenk Balaban","Ceren Aygüzen","Ceren Aydın","Cevat Çelebi","Cevher Çeliköz","Cihat Çınar","Cuma Polat","Davut Küçükoğlu","Deniz Eski","Dentista Klinik","Dentoria Ağız Ve Diş Sağlığı, Ağız Ve Diş Sağlığı,","Derya Öznam Eke","Derya Dursun Diktas","Derya Mayir","Derya Inanlı","Derya İvgen Aydın","Devrent Ağız Ve Diş Sağlığı","Diler Nizam","Diş Levent","Diş Ve Diş Poliklinik","Duran Çelik","Dursun Yeşilyurt","Ebhun Arkadaş","Ebrahim Paknahad","Ebru Ispirgil","Ebru Akgül","Ebru Armutlu","Ebru Günday","Elif Delen Şahin","Emel Soydan","Emel Çakır","Emine Uysal Yılmaz","Emre Tülü","Emre Armutlu","Ercan Taş","Erdal Isik","Erdem Köse","Erdem Bulut Dur","Erdinç Sakir","Erdoğan Ertek","Erem İlkay","Erhan Görükmez","Erhan Gürsoy","Erkan İşman","Erkan Gün","Erol Cinar","Erol Atalay","Ertan Toprakhisar","Ertuğrul Üstek","Esen Aydoğdu","Esra Karaca","Ethem Has","Evren Özdemir","Eyüp Ak","Ezgi Yeşim Kizil","Fadıl Ilgın","Fahrettin Kabataş","Faruk Mercan","Fatih Kaya","Fatih Kozan","Fatma Türel","Fatma Yenice","Fatma Pehlivan Çakmakçı","Fatma Çiğdem Üzel","Ferda Üstün","Ferit Dönmez","Fetih Düzgen","Fevziye Karakol Dönmez","Figen Sengul","Fikret Değer","Fikri Genç","Filiz Kavuşturan","Filiz Yağbasan","Filiz Zeybek","Funda Öz Okan","Furkan Başak","Gizem Terzioğlu","Gökçen Karatasli","Göknur Gözen","Göral Ağiz Ve Diş Sağliği Kliniği","Gözde Katmer","Gül Oskaylar","Gülden Mut Bekerecioğlu","Gülfeza Pamuk Hindioğlu","Gülşen Erdinç Öztürk","Gülşen Karataş Aydın","Gülsüm Ozsagdic","Gülten Hayir Akca","Gülver Ceylan","Günay Baş","Gurkan Gunce","Gürkan Günçe","Halil Korkmaz","Halil Dokuyucu","Halil Gürsel Ayşit","Halit Buyukogut","Harun Koca","Harun Fansa","Hasan Bereket","Hasan Çağrıhan Ermeydan","Hasan Hüsnü Eriş","Hayal Akbulut","Hayrani Tabak","Hayrettin Kılavuz","Hızır Baş","H&M Dent Klinik","H. Necdet Peskircioglu","Hüdayi Boğahan","Hülya Polater","Hülya Erkek","Huriye Karabacak","Huseyin Erdogan","Hüseyin Meşeci","Hüseyin Cahit Dursun","Hüsmen Ayan","İbrahim Hepdarcan","İdris Onur","İhsan Bey Şehabettin Tuna Kliniği","İlhan Karataş","İncisin Diş","İrem Güler Turunç","İrfan Ercihan","Isa Nuh","Işıl Gün","İsmail Yalçın","Kahraman Gürcan","Kemal Ömür","Kenan Gültekin","Kenan Nazaroğlu","Kerem İşigüzel","Kurtuluş Özmen","Kurtuluş Savaş Şimşek","Mahir Yücel","Mahir Çataltepe","Mahmut Kemal Nalbantoğlu","M.Can Polat","Mehmet Özçomak","Mehmet Tuncer","Mehmet Altun","Mehmet Karaboğa","Mehmet Ali Yavan","Mehmet Ali Demirhan","Mehmet Yücel Özbaş","Mehtap Atılgan","Menekşe Urcan","Merih Şişik","Meryem Şahin","Meryem Murat","Michalle Demirağ","Midhat Boz","Muhammed Şerif","Muhammed Kouja","Muharrem Armutlu","Muhsin Mustafa","Murat Çavuş","Murat Papak","Murat Çiteli","Mustafa Diri","Mustafa Ozan Güldoğan","Mustafa Ahmet","Mustafa Şamil Asal","Muzaffer Kılıç","Müzeyyen Özyavuz","Nafi Akın","Necati Kemal","Necla Sezen","Nehire Rodoplu","Nesrin Özgön","Nesrin Akan Küçük","Nevzat Tabak","Nilay Oral","Nilgün Arat Cabıoğlu","Nilüfer Karaselçuk","Nilüfer Emel Umut","Nimet Aslı Südoğan","Nuran Sevdi Kıskanç","Nurefşan Evli","Nurhan Erkal Bor","Ömer Haluk Elçioğlu","Önder Çalışkan","Onur Şengezer","Oral Sökücü","Orhan Aksoy","Osman Binan","Özel Avrupa İnci Ağız Ve Diş","Özel Hayri Öztürk Diş Kliniği","Özel Seçkin Ağiz Ve Diş Sağliği Polikliniği","Özgül Deveci","Özgür Başar Varoğlu","Özkan Bayar","Özlem Halisdemir","Pamir Meric","Pelin Eren","Pınar Şeşen","Ramazan Oltan","Recep Üstün","Resul Borahan","Riyad Aslan","Rojbin Kahraman","Ruhengiz Efendiyeva","Rümeysa Ömer","Rüstem Beyaz","Sabiha Gökçe Kelce","Saeed Pezeshk","Saime Dilara Peker","Sait Yıldız","Salih Hazır","Salih Cihat Beşar","Salim Doğan","Salim Bayram","Salman Temtek","Sami Aksoğan","Saniye Özen","Sedat Taşo","Sedef Ağcabay Ersöz","Sefa Arslan","Seher Yeşildal","Selçuk Aydin","Selim Ersanlı","Sema Demir","Semadent Diş","Semahat Arslan","Semih Gürbüz","Semir Şakar","Şennur Çağlar","Serap Serhatlı","Serçin Çürükova Ofluoğlu","Serdar Yalçın","Serhan Aktan","Serhan Dönmez","Sibel Şen","Simge Öncü","Sonay Öztan Gökhan","Suat Erdem Torğutalp","Suzan Özel","Taha Yaşar Manav","Taner Alagöz","Taner Ajar","Taşkın Türker","Tevfik Altuncu","Tufan Kar","Tuğba Bulut","Tuğçe Atçakan","Turgay Emekli","Turgut Dindaroğlu","Türkan Kaçar","Uğur Güzey","Uğur Aksoy","Uğur Baykal","Vedat Eren","Veli Kala","Volkan Güngör","Yakup Uğur Özdemir","Yaşar Yıldırım","Yasemin Delikan Topçu","Yasemin Gençtarih","Yasemin Erdogan","Yılmaz Cebecioğlu","Yılmaz Tanrıbuyurdu","Yüksel Üzel","Yusuf Murat Kılıç","Yusuf Atuğ","Yusuf Küçük","Yusuf Sert","Yusuf Kaya","Yusuf Doğar","Zafer Tel","Zeki Özalp","Zerrin Küpçü","Zeynep Kuruköse","Zeynep Füsun Yücel","Ziryan Jaza Hamasalih"]
        array= Doctor.objects.all()
        context['doctors'] = array
        for d in array:
            if d.account.get_full_name() in doctors_list:
                d.miy=context['buse']
                d.save()
                return(d.account.get_full_name(),d.miy)
        return context

#kontrol ettim
#ID'leri çekmek lazım, Account hatası önemsiz, Template view'e çevirdim ListViewden bir bakmak lazım
class DoktorTakimEsleme(TemplateView):
    context_object_name = 'doktor_takim_esleme'
    template_name = 'seffaf/doktor_takim_esleme.html'
    monday= timezone.now().replace(microsecond=0,hour=0,minute=0,second=0)  - timedelta(90)
    queryset = Doctor.objects.filter(signup_time__gte= monday).select_related('account').select_related('miy').select_related('miy__account').order_by('-signup_time')

    def get_context_data(self, **kwargs):
        context = super(DoktorTakimEsleme, self).get_context_data(**kwargs)
        Druid_miys = [EZGI_MIY_ID,OZLEM_MIY_ID]
        Druid_anatec = Account.objects.get(pk = ESIN_ID)
        
        Shaman_miys = [VILDAN_MIY_ID,BASAK_MIY_ID]
        Shaman_anatec = Account.objects.get(pk = NIMET_ID)
    
        Mage_miys = [BUSE_MIY_ID,DENIZ_MIY_ID]
        Mage_anatec = Account.objects.get(pk = BERKAY_ID)
        
        Paladin_miys = [SINEM_MIY_ID, ZEYNEP_MIY_ID]
        Paladin_anatec = Account.objects.get(pk = ABDULLAH_ID)

        Druid_doctors = Doctor.objects.filter(miy__pk__in = Druid_miys)
        Shaman_doctors = Doctor.objects.filter(miy__pk__in = Shaman_miys)
        Mage_doctors = Doctor.objects.filter(miy__pk__in = Mage_miys)
        Paladin_doctors = Doctor.objects.filter(miy__pk__in = Paladin_miys)

        counter= 0 
        context['counter']=counter
        context['Druid_doctors']=Druid_doctors
        context['Shaman_doctors']=Shaman_doctors
        context['Mage_doctors']=Mage_doctors
        context['Paladin_doctors']=Paladin_doctors
        
        for doctor in Druid_doctors:
            doctor.anatec = Druid_anatec
            counter += 1
            print(counter)
            doctor.save()
       
        for doctor in Shaman_doctors:
            doctor.anatec = Shaman_anatec
            counter += 1
            print(counter)
            doctor.save()
        
        for doctor in Mage_doctors:
            doctor.anatec = Mage_anatec
            counter += 1
            print(counter)
            doctor.save()
        
        for doctor in Paladin_doctors:
            doctor.anatec = Paladin_anatec
            counter += 1
            print(counter)
            doctor.save()
        
        return context

#line 163
class DoktorUretimciDegistirme(TemplateView):
    context_object_name = 'doktor_uretimci_degistirme'
    template_name = 'seffaf/doktor_uretimci_degistirme.html'
    monday= timezone.now().replace(microsecond=0,hour=0,minute=0,second=0)  - timedelta(90)
    queryset = Doctor.objects.filter(signup_time__gte= monday).select_related('account').select_related('miy').select_related('miy__account').order_by('-signup_time')

    def get_context_data(self, **kwargs):
        context = super(DoktorUretimciDegistirme, self).get_context_data(**kwargs)
        MAHIR_ID=2633
        SERAY_ID=3192
        SERAP_ID=2900
        ECE_ID=2634
        SERHAT_ID=3562
        #Doctor protec değiştirme 
        miy=MIY.objects.get(id=7)
        analyser=Account.objects.get(id=2385)
        
        miy_producer =[ [ MIY.objects.get(id=SINEM_MIY_ID),Account.objects.get(id=SERHAT_ID) ],
                        [ MIY.objects.get(id=BASAK_MIY_ID),Account.objects.get(id=SERAY_ID) ],
                        [ MIY.objects.get(id=DENIZ_MIY_ID),Account.objects.get(id=SERAP_ID) ],
                        [ MIY.objects.get(id=OZLEM_MIY_ID),Account.objects.get(id=MAHIR_ID) ],
                        [ MIY.objects.get(id=EZGI_MIY_ID),Account.objects.get(id=MAHIR_ID) ] ]
            #print (miy,analyser)
        array= Doctor.objects.all().select_related('miy__account').select_related('protec')
        array2=[]
        for d in array:

        #    if(d.anatec):
        #        print (d.anatec.get_full_name())
            for team in miy_producer:
            
                if(team[0] == d.miy):
                    #print (team[0])
                    producer=team[1]

                    if(producer != d.protec ):    
                        print ("--------")
                        array2.append(d.account.get_full_name() + '- ' + d.miy.account.get_full_name() +'-' +producer.get_full_name() + '-' + str(d.protec))
                        d.protec=producer
                        d.save()
                        print (d.account.get_full_name())
                        print (d.protec.get_full_name())

            
        print ("adet",len(array2))
        context['array2'] = array2
        context['producer'] = producer
        context['array'] = array
        context['user'] = self.request.user
        context['logs'] = LogEntry.objects.filter(user=2039).order_by('action_time')
        context['logs'] = Case.objects.filter(created__lte=timezone.now().replace(month=12,day=1,microsecond=0,hour=0,minute=0,second=0) )\
                                        .filter(created__gte=timezone.now().replace(month=10,day=1,microsecond=0,hour=0,minute=0,second=0) )\
                                        .select_related('doctor').select_related('doctor__account').order_by('-created')
        context['count'] =  context['logs'].count()
        return context


            
