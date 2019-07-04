from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Account(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    last_version = models.IntegerField(default = 0)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateField( blank=True,null=True)
    tagline = models.CharField(max_length=140, blank=True)
    cellphone =  models.CharField(max_length=20)
    picture = models.CharField(max_length=160,default="user.jpg") #models.CharField(max_length=160,default="http://seffafcdn.blob.core.windows.net/profilepics/user.jpg")
    source = models.CharField(max_length=40,default="web")
    push_token  = models.CharField(max_length=300,blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    all_accounts = models.Manager()
    kvkk_onay=models.NullBooleanField(blank=True,null=True)
    kvkk_onay_date=models.DateTimeField(blank=True,null=True)
    kvkk_ip = models.CharField(max_length=40)
    
    #anatec ratios
    target_ratio_new = models.DecimalField(max_digits=3, decimal_places=2, default=2)
    target_ratio_control = models.DecimalField(max_digits=3, decimal_places=2, default=0.75)

    #protec ratios
    target_ratio_mumlu = models.DecimalField(max_digits=3, decimal_places=2, default=2.5)
    target_ratio_mumsuz = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)

    roles = (
        ('doctor', 'Doktor'),
        ('admin', 'Admin'),
        ('head' ,'Yönetici'),
        ('miy', 'MIY'),
        ('hunter', 'Satış Elemanı'),
        ('anatec', 'Analiz Teknisyeni'),
        ('modtec', 'Model Teknisyeni'),
        ('protec', 'Üretim Teknisyeni'),
        ('pritec', 'Printer Teknisyeni'),
        ('stotec', 'Depolama Sorumlusu'),
        ('adviser','Danışman Hekim'),
        ('presen' ,'Satış Temsilcisi '),
        ('investor' ,'Yatırımcı'),
        ('distributor' ,'Distribütör'),
        ('ctrltec' ,'Kalite Kontrol Teknisyeni'),
        ('clinic' ,'klinik'),


    )
    
    role = models.CharField(
        max_length=12,
        choices=roles,
        default='doctor',
    )

    language = models.CharField( max_length=5, blank=True,null=True,default='tr') 
    #country = models.CharField( max_length=35,choices = COUNTRYS,default='Türkiye') 

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_active_mail = models.BooleanField(default=True)
    is_jr = models.BooleanField(default=False)
    
    created     = models.DateTimeField()
    modified    = models.DateTimeField()

    #objects = AccountManager()

    opens_account_id = models.CharField(max_length=10,blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

class Case(models.Model): 
    
    class Meta:
        ordering = ['created']
        
    anatec= models.ForeignKey(Account,on_delete=models.SET_NULL, related_name='anatec',blank=True,null=True,limit_choices_to={'role': 'anatec'},)
    protec= models.ForeignKey(Account,on_delete=models.SET_NULL, related_name='caseprotec',blank=True,null=True,limit_choices_to={'role': 'protec'},)
    segtec= models.ForeignKey(Account,on_delete=models.SET_NULL, related_name='segtec',blank=True,null=True,limit_choices_to={'role': 'anatec'},)
    meshtec= models.ForeignKey(Account,on_delete=models.SET_NULL, related_name='meshtec',blank=True,null=True,limit_choices_to={'role': 'anatec'},)
    # doctor = models.ForeignKey(Doctor, on_delete=models.SET_DEFAULT,default=1)
    # adviser = models.ForeignKey(Adviser, on_delete=models.SET_DEFAULT,default=1)
    # processing = models.ManyToManyField(Processing,blank=True)
    case_id = models.CharField(max_length=20,blank=True,null=True)
    invoice_id = models.CharField(max_length=20,blank=True,null=True)
    onay=models.BooleanField(default=False)
    onay_date= models.DateTimeField(blank=True,null=True)
    distributor_onay=models.BooleanField(default=False)
    distributor_onay_date= models.DateTimeField(blank=True,null=True)
    paid_date=models.DateTimeField(blank=True,null=True)
    last_status_title= models.IntegerField(default=1,blank=True,null=True)
    last_status_created= models.DateTimeField(blank=True,null=True)
    last_status_htmltitle= models.CharField(max_length=50 ,default= 'Ölçü Bekleniyor')
    last_status_htmltag= models.CharField(max_length=50 ,default='label-default')

    # cargo_address = models.ForeignKey(Address,on_delete=models.SET_NULL, related_name='cargo_address',blank=True,null=True,)
    # invoice_address = models.ForeignKey(Address,on_delete=models.SET_NULL, related_name='invoice_address',blank=True,null=True,)

    anatec_start  =  models.DateTimeField(blank=True,null=True) 
    anatec_finish =  models.DateTimeField(blank=True,null=True)
    
    #Patient Information
    patient_name = models.CharField(max_length=50)
    patient_lastname = models.CharField(max_length=50)
    patient_age = models.IntegerField(default=0,blank=True,null=True)
    patient_birthday= models.DateTimeField(blank=True,null=True)
    gender = (
        ('1', _('Erkek')),
        ('2', _('Kadın')),
    )
    patient_gender = models.CharField(max_length=10,choices=gender,default=1)

    operation_array = (
        ('1', 'İşlemli Ölçü Değil'),
        ('2', 'Kesin Retainer'),
        ('3', 'Retainer Olabilir'),
        ('4', 'Plak Basılacak'),
    )

    operation_status= models.CharField(max_length=1,choices=operation_array,default='1')

    jaw_array = (
        ('1', _('Üst')),
        ('2', _('Alt')),
        ('3', _('Üst-Alt')),
    )
    jaw = models.CharField(max_length=20,choices=jaw_array,default=3)

    #Existing Conditions TANI
    main_request = models.TextField(blank=True,null=True)
    dentition = models.CharField(max_length=20,choices=(('1', _('Sürekli')),('2', _('Karışık')),),default=1)
    midline_array = (
        ('1', _('+2mm Sağ')),
        ('2', _('1-2mm Sağ')),
        ('3', _('0-1mm Sağ')),
        ('4', _('Uyumlu')),
        ('5', _('0-1mm Sol')),
        ('6', _('1-2mm Sol')),
        ('7', _('+2mm Sol')),
    )
    upper_midline= models.CharField(max_length=20,choices=midline_array,default=4)
    lower_midline= models.CharField(max_length=20,choices=midline_array,default=4)

    midline_array_new = (
        ('1', _('Koru')),
        ('2', _('İyileştir')),
    )

    upper_midline_new= models.CharField(max_length=20,choices=midline_array_new,default=1)
    lower_midline_new= models.CharField(max_length=20,choices=midline_array_new,default=1)
    
    relationship_array = (
        ('1', _('Sınıf I')),
        ('2', _('Sınıf II')),
        ('3', _('Sınıf III')),
    )
    right_canine_relationship= models.CharField(max_length=20,choices=relationship_array,default=1)
    left_canine_relationship= models.CharField(max_length=20,choices=relationship_array,default=1)
    
    right_molar_relationship= models.CharField(max_length=20,choices=relationship_array,default=1)
    left_molar_relationship= models.CharField(max_length=20,choices=relationship_array,default=1)
    overjet_now= models.DecimalField(max_digits=8, decimal_places=2,default=0)
    overbite_now= models.DecimalField(max_digits=8, decimal_places=2,default=0)
    
    #Tedavi Planlama
    instruction1_array = (
        ('1', _('Koru')),
        ('2', _('İyileştir')),
        ('3', _('İdealleştir')),
    )

    need_help = models.BooleanField(default=False)
    upper_midline_exp = models.CharField(max_length=20,choices=instruction1_array,default=2)
    lower_midline_exp = models.CharField(max_length=20,choices=instruction1_array,default=2)
    overjet       = models.CharField(max_length=20,choices=instruction1_array,default=2)
    overbite      = models.CharField(max_length=20,choices=instruction1_array,default=2)
    canine_relationship = models.CharField(max_length=20,choices=instruction1_array,default=2)
    molar_relationship  = models.CharField(max_length=20,choices=instruction1_array,default=1)
    posterior_cross_closing  = models.CharField(max_length=20,choices=instruction1_array,default=1)

    instruction2_array= (
        ('1', _('Öncelikli')),
        ('2', _('Gerekliyse')),
        ('3', _('Hayır')),
    )
    instruction3_array = (
        ('1', _('Koru')),
        ('2', _('Genişlet')),
    )
    upper_ipr       = models.CharField(max_length=20,choices=instruction2_array,default=1)
    upper_procline  = models.CharField(max_length=20,choices=instruction2_array,default=2)
    upper_arc_form = models.CharField(max_length=20,choices=instruction3_array,default=1)
    #upper_expand    = models.CharField(max_length=20,choices=instruction2_array,default=1)
    upper_distalize = models.CharField(max_length=20,choices=instruction2_array,default=2)
    
    lower_ipr       = models.CharField(max_length=20,choices=instruction2_array,default=1)
    lower_procline  = models.CharField(max_length=20,choices=instruction2_array,default=2)
    lower_arc_form = models.CharField(max_length=20,choices=instruction3_array,default=1)
    #lower_expand    = models.CharField(max_length=20,choices=instruction2_array,default=1)
    lower_distalize = models.CharField(max_length=20,choices=instruction2_array,default=2)
    
    #Additional Instructions
    # dont_move = models.ManyToManyField(Tooth,blank=True,related_name='dont_move')
    # avoid_engagers = models.ManyToManyField(Tooth,blank=True,related_name='avoid_engagers')
    # extract_teeth = models.ManyToManyField(Tooth,blank=True,related_name='extract_teeth')
    # leave_space = models.ManyToManyField(Tooth,blank=True,related_name='leave_space')
    # patient_diastemas =  HStoreField(blank=True, null=True)
    # special_instructions=  models.TextField(blank=True)
    
    paid=models.BooleanField(default=False)
    cancelled=models.BooleanField(default=False)
    case_diff = models.IntegerField(default=0,null=True,blank=True)
    link = models.CharField(max_length=300,null=True,blank=True)
    #case_type= models.CharField(max_length=20,choices=STATIC_CASE_TYPE,default=1,null=True,blank=True)
    is_active= models.BooleanField(default=True)
    is_reimpresion = models.BooleanField(default=False)
    is_star = models.BooleanField(default=False)
    is_control =models.BooleanField(default=False)
    is_precomment=models.BooleanField(default=False)
    is_default_values_change= models.BooleanField(default=False)
    is_missinginfo= models.NullBooleanField()
    is_promo= models.NullBooleanField()
    is_cross_border = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    start_delivery= models.DateTimeField(blank=True,null=True)
    analysis_delivery= models.DateTimeField(blank=True,null=True)
    order_delivery = models.DateTimeField(blank=True,null=True)
    analysis_delivery_end= models.DateTimeField(blank=True,null=True)
    order_delivery_end = models.DateTimeField(blank=True,null=True)
    is_urgent = models.DateTimeField(blank=True,null=True)
    #objects = with_undeleted()
    all_cases = models.Manager()
    is_QualityControlSampleCase = models.BooleanField(default=False)
    
    case_create_steps = (
        ('0', _('Hasta Bilgileri')),
        ('1', _('Reçete Oluştur')),
        ('2', _('Fotoğraf Yükle')),
        ('3', _('Panoramik Yükle')),
        ('4', _('İntraoral & Pvs Ölçü Gönder')),
        ('5', _('Tamamla')),
    )
    case_create_step = models.CharField(max_length=30,choices=case_create_steps,default=0)

    created     = models.DateTimeField()
    modified    = models.DateTimeField()



