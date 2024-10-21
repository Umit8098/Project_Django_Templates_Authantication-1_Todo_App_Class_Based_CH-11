
#### Baştan proje kurulumu ->

```bash
- python -m venv env
- ./env/Scripts/activate
- pip install django
- python.exe -m pip install --upgrade pip
- pip freeze
- pip install python-decouple
- pip freeze > requirements.txt
```

```bash
- django-admin startproject main .
- py manage.py runserver
- py manage.py startapp user_example

```

## Secure your project

### .gitignore

Add standard .gitignore file to the project root directory. 

Do that before adding your files to staging area, else you will need extra work to unstage files to be able to ignore them.

<.gitignore> ->

```py
# Environments
.env
.venv
env/
venv/
```


### python-decouple

- Create .env file on root directory. We will collect our variables in this file.

<.env> ->

```py
SECRET_KEY = django-insecure-9p72pxko$)cm=wwzt81kg*6u-%#j*iyxhens02^96bw&iq2idn
```

<settings.py> ->

```py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

- From now on you can send you project to the github, but double check that you added a .gitignore file which has .env on it.


- Run the server and see the initial setup:
 
```bash
py manage.py migrate
```

```bash
py manage.py runserver  # or;
python manage.py runserver  # or;
python3 manage.py runserver
```

///////////////////////////////////////////////////
#### GİTHUB REPODAN clone bir projeyi ayağa kaldırma ->

```bash
- python -m venv env
- ./env/Scripts/activate
- pip install -r requirements.txt
- python.exe -m pip install --upgrade pip
- pip install python-decouple
- pip freeze > requirements.txt
```

- create .env and inside create SECRET_KEY 

```bash
- python manage.py migrate
- python manage.py runserver
```

///////////////////////////////////////////////////

- Projeyi ve app imizi oluşturduk, .gitignore ve .env dosyalarımızı da oluşturup SECRET_KEY imizi ve env ımızı içerisine koyduk.
- app imizi settings.py daki INSTALLED_APPS e ekliyoruz.
  
```py
  INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # myApps
    'user_example',
]
  ```

-  ana urls.py ımıza app imizin urls.py ını include ediyoruz. Hemen sonra user_example app imizin urls.py ını create ediyoruz.
-  
main <urls.py> ->

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("user_example.urls")),
]
  ```

- app imizin views.py ında basit bir home view i oluşturup bize user_example app imizin altındaki index.html template i döndürmesini yazıyoruz.

user_example <views.py> ->

```py
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'user_example/index.html')
```

- view imizin path ini oluşturuyoruz;

user_example <urls.py> ->

```py
from django.urls import path
from .views import home

urlpatterns = [
    path('', home, name='home'),
]
```

- Şimdi home view imizin index.html template ini user_example app imizin altında oluşturacağmız templates klasörünün altında yine app imizin ismiyle oluşturacağımız  user_example klasörü içerisinde index.html olarak oluşturuyoruz.

templates/user_example/index.html - >

```html
{% if user.is_authenticated %} 
<h1 style="text-align: center; color:red; margin-top: 5rem;">
    Hello {{user.username | title}}    
</h1>

{% comment %}
<a href="{% url 'logout' %}">Logout</a>
{% endcomment %}
    

{% else %}
<h1 style="text-align: center; color:purple; margin-top: 5rem;">
    Hello, please login to see the page.
</h1>

{% comment %}
<a href="{% url 'login' %}">Login</a> 
{% endcomment %}
    

{% endif %}

```

- Burada basit bir if condition kuruyoruz, kullanıcı authenticate ise; kullanıcının ismini büyük harfle çekip hello diyor. Eğer authenticate değilse; hello sayfayı görmek için login olun diyor. Bir de login ve logout linkleri yerleştirilmiştir.

- index.html içerisindeki user değişkeni django bize otomatik olarak veriyor. Yani o andaki user ı bu şekilde template imizde görebiliyoruz. default olarak geliyor. Bunu herhangi bir view içerisinde context içerisinde göndermek zorunda değiliz.

```bash
- python manage.py createsuperuser
- python manage.py createsuperuser --username admin --email umit@gmail.com
```

- superuser oluşturup admin panelden giriş yapınca home view imizin render ettiği index.html template indeki if condition u çalışıyor ve bizi artık login olmuş olarak karşılıyor (Hello Admin) 

### The Django Authentication Models

Django.contrib.auth.models has 
- User, 
- Permission,
- Group Models,

Bu, bir kullanıcıyı, sahip oldukları herhangi bir grup ve izinle birlikte o kullanıcı hakkında bazı kalıcı verilerle ilişkilendirmeye yarar.

- best practice olarak bir grup oluşturulur ve o gruba permissions lar tanımlanır, user lar o gruba konulur. Böylece daha sade ve kolay bir kullanım oluyor.

### Add user programmatically
- CLI (Command Line Interface) da bazı işlemleri yapmak demektir. user create edebiliriz.
- user modelinin create_user() diye bir methodu var, içerisine username, email, password, .. staff  gibi bunları tek tek konulabiliyor. username positional argument, email, password, .. stuf bunlar keyword argument olarak eklenebiliyor.
- Bu bize çok hızlı veri create etmemizi sağlıyor. Mesela bir personel listesi çektiniz biryerden, bunu user olarak db ye eklememiz lazım, bir for döngüsü yazarsınız , içine user modelini çağırıp tek tek gelen değerleri create_user() method unun içine atarsınız, dakikalar içerisinde binlerce user create edebilirsiniz. Bize sağladığı en büyük kolaylıklarından birisi hızdır.

shell ile bir interactive console  açıyoruz. shell djangoya özgü bir python consolu dur. 

```bash
- py manage.py shell
- exit()  # shell den çıkış komutudur.
```

shell console da djangoya gömülü User modelini import ediyoruz. django default olarak django.contrib.auth.models içinde oluşturulmuş olan User modelilini kullanıyor. Bu User modelinin fieldlarını biz admin panelde görebiliyoruz.

```bash
- from django.contrib.auth.models import User
- user1 = User.objects.create_user('umit', email='u@u.com')
- user2 = User.objects.create_user('john', email='lennon@thebeatles.com', password='johnpassword', is_staff=True)

```
komutlarıyla umit diye bir kullanıcı create ettik. Create ederken .save() istemiyor. Ancak extra bir field ekleyeceğimiz zaman .save() istiyor; 

```bash
- user1.first_name = 'Emirhan'
- user1.save()
```
her seferinde admin panele gidip kontrol ediyoruz.

bir user ı password girmeden de create edebiliyoruz. Daha sonradan user a bir password atamak için set_password('new password') kullanıyoruz. Bu db ye sha256 ile hash lenmiş bir şekilde kaydedilmesini sağlıyor.

```bash
- user1.set_password('umit123456')
- user1.save()
```

#### Authentication Views

https://docs.djangoproject.com/en/4.1/topics/auth/default/

- Django, oturum açma, oturum kapatma ve parola yönetimini yönetmek için kullanabileceğiniz çeşitli görünümler sağlar.

- Bunun için yapılması gereken main/urls pathern e şu kısmın eklenmesi; ->

main/urls.py
```py

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
]

```

- Bu patern projenin urls.py'ınada eklenebilir,  app imizin urls.py ına da eklenebilir. Şimdi biz burada projenin urls.py ına değil de user app'imizin urls.py ına ekledik.
- Ancak app'in urls.py'ına eklenirse çok sıkıntı çıkarıyor (password_change, change_done işlerinde). O yüzden main/urls.py'da olması daha sağlıklı.

main <urls.py> ->

```py
from django.urls import path, include
from .views import (
    home,
)

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]
```
- Django.contrib.auth.urls'e bakarsanız, tanımlanmış varsayılan görünümleri görebilirsiniz. Bu oturum açma, oturum kapatma, password_change ve password_reset olacaktır.
- Djangonun django.contrib.auth.urls unun içinde urls leri var. Bu urls ler bizi djangonun hazır oluşturulmuş views lerine yönlendiriyor, o view ler de belli başlı template lere yönlendiriyor. ->

- http://127.0.0.1:8000/accounts/ URL'sine gidin (sondaki eğik çizgiye dikkat edin!) ve Django bu URL'yi bulamadığı ve denediği tüm URL'leri listelediği bir hata gösterecektir. Bundan çalışacak URL'leri görebilirsiniz.

- Yukarıdaki yöntemin kullanılması, URL eşlemelerini tersine çevirmek için kullanılabilen köşeli parantez içinde adları olan aşağıdaki URL'leri ekler. Başka bir şey uygulamanız gerekmez - yukarıdaki URL eşlemesi, aşağıda belirtilen URL'leri otomatik olarak eşler.


Bu, aşağıdaki URL modellerini içerecektir:
```py
- accounts/login/ [name='login']
- accounts/logout/ [name='logout']
- accounts/password_change/ [name='password_change']
- accounts/password_change/done/ [name='password_change_done']
- accounts/password_reset/ [name='password_reset']
- accounts/password_reset/done/ [name='password_reset_done']
- accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
- accounts/reset/done/ [name='password_reset_complete']
```

- Biz bu djangonun bize sağladığı default değerler üzerinden gideceğiz.

- proje klasöründeki main/urls.py'a gidip accounts/ path ini ekliyoruz.

main/urls.py
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_example.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

- Yani bize domain url imize accounts diye birşey gelirse, beni django.contrib.auth.urls e yönlendiriyor. Kütüphaneden django.contrib.auth.urls e giderek viewsleri de gördük.

- path e accounts/ koyduktan sonra bakalım bize ne veriyor. tarayıcıya gidip accounts/ yazıp bakıyoruz.

- login, password_change , password_reset gibi templateleri kullanabilmemiz için template klasörü oluşturup onan altında registration isimli bir klasör oluşturup onun içine templatelerimizi dokümanda yazdığı isimlerle yazmamız gerekiyor. Dokümantasyondan bakıyoruz bunlara. 
- Tabi bu template lerin form u da view i de hazır. Nerde hazır? django.contrib.auth un içerisinde. bunları kullanmamız için bizim sadece template hazırlamamız gerekiyor.

##### Login Template
- login template imizle başlıyoruz. 

- app imizin altında templates klasörünün altına registration diye bir klasör oluşturup içine dokümantasyonda yazdığı şekliyle login, password template lerimizi buraya kaydediyoruz.

- login template imizi template/registration/login.html şeklinde create ediyoruz. Burada bize login olmamız için kullanıcıdan login bilgilerini alacağımız bir form lazım. Bu form djangonun default olarak hazırlamış olduğu login_view ile sağladığı formudur. Biz bu formu sadece template imizde render ediyoruz. -> 

templates/registration/login.html ->
```html
    <form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Login">
    </form>
```

- Evet login sayfamız geldi. (accounts/login).  Burada bu template için view yazmadık çünkü default olarak tanımlı bir login view i var ve django onu kullanıyor.

- formu render ettiğimiz zaman yani Login inputuna bastığımız zaman bizi otomatik olarak accounts/profile diye bir sayfaya redirect ediyor.

- Ancak bizim profile diye bir sayfayamız template imiz yok. Belki de oluşturmak da istemiyoruz, djangonun bu default ayarını kullanmak istemiyoruz. Bunu için settings.py a gidip LOGIN_REDIRECT_URL = "/" kodunu en alta yazıyoruz ve içerisine login olduktan sonra nereye yönlendirmek istiyorsak o path in dinamik name ini yazıyoruz.
- Burada 'user_example' app'imizin 'home' page'ine yönledirmek istiyoruz.
  
<settings.py>
```py
LOGIN_REDIRECT_URL = "home"
```

- Bu sayede login page de Login butonu ile sayfayı render ettiğimizde bizi default profile sayfasına değil de bizim settings.py da LOGIN_REDIRECT_URL ile belirttiğmiz home page e yönlendirmesini sağladık.

- ÖZET : Ben senin için bazı view ler ve url ler hazırladım. Onları kullanarak çok hızlı bir şekilde authenticate sistemini kurabilirsin. Bunlar ne? login, logout, password_change, password_reset. 
- Ama bunları kullanabilmen için url paternine 'accounts/', include('django.contrib.auth.urls') path ini eklemelisin ki default ayarlarımı sana sunabileyim. 
- Bize default olarak view ve url sunuyor ama template leri bizim hazırlamamızı bekliyor. default ayarlarına göre istediği template leri de registration klasörünün altında istiyor. Biz de app imizin altında templates klasörünün altında registration klasörü oluşturup template lerimizi bu klasörün içine dokümanın bizden istediği isimle oluşturuyoruz. login template ini oluşturduktan sonra ve login olmaya çalıştıktan sonra yine django default olarak profile diye bir sayfaya redirect etmeye çalışıyor. Biz login olduktan sonra redirect olarak nereye gitmek istiyorsak onu belirtmek için settings.py da LOGIN_REDIRECT_URL = "home" yazarak bunu belirtiyoruz. 

###### urlpatterns'e app_name verme;
- DİKKAT!!!
- django bazen (genelde) redirect edilmek istenen page'i bulamayabilir. Bunun çözümü için redirect edilmek istenen page'in bulunduğu urlpatterns'e app_name='name' verilerek, ve bu name'i de page'in önünde kullanarak djangoya redirect edilmek istenen page'i tam olarak gösterebiliriz.
 - urls.py'da urlpatterns'nin hemen üzerinde app_name = 'name' şeklinde isimlendirme yapıp, redirect edeceğimiz page name'lerini de 'name:home' şeklinde yazmamız gerekiyor.

user_example/urls.py
```py
...

app_name = 'user_example'

urlpatterns = [
    ...
]
```

- Aynı şekilde settings.py'da ayarlamış olduğumuz redirect edilecek page'in formatı da şu şekilde olması gerekiyor.
 LOGIN_REDIRECT_URL = "user_example:home"

main/settings.py
```py
...
LOGIN_REDIRECT_URL = "user_example:home"
...

```


##### Registration view and Create User

- user eklemeyi admin panelden yapıyoruz, ama login i login template inden yapıyoruz, çok mantıklı değil. Şimdi user ı kendi frontent'imizden create etmemiz lazım.
- djangonun bize sağlamadığı tekşey registration. registration view ini biz kendimiz yazacağız.
- Register işlemini djangonun bize sunduğu UserCreationForm() diye bir form var buradan yapacağız.Bu forma ekleme çıkarma da yapabiliyoruz.
- django.contrib.auth.forms dan UserCreationForm u import ediyoruz, ve register view imizi yazıyoruz. UserCreationForm() dan boş bir form alıp form değişkenine tanımlıyoruz. Bu boş form u da context içinde template imize gönderiyoruz.

user-example/views.py
```py
from django.contrib.auth.forms import UserCreationForm

def register(request):
    form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)
```

- Arkasından app imizin url listesine register view imizi ekleyip, register page imizi create ediyoruz;

user_example/urls.py
```py
from django.urls import path
from .views import (
    home,
    register,   
)

app_name = 'user_example'

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
]
```

- Son olarak register.html template imizi içinde formumuz olacak şekilde yazıyoruz.

templates/register/register.html
```html
<h1>Registration Page</h1>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Register">
</form>
```

///////////////////////////////////////////////////////////
- NOT : user_example app i bir authentication application ıdır. Bu app i kopyalayıp diğer projeye koyup, projenin urls.py ına da
  path('accounts/', include('django.contrib.auth.urls')),
path ini ekleyip, settings.py ına da
  LOGIN_REDIRECT_URL = "home"
  veya urlpatterns name_space ile 
  LOGIN_REDIRECT_URL = "user_example:home"

ekleyip hazır bir authentication sistemi olarak kullanabiliriz.
///////////////////////////////////////////////////////////

- register template imizi gördük. Fakat viewimizde bir algoritma kurmadık. View imiz şuanki haliyle eksik. 
- Formun içinde gelen bilgileri bizim kaydetmemiz, ardından bir yere redirect etmemiz gerekiyor. 

- UserCreationForm(request.POST or None) ile post ise, 
 - form is valid 
 - form save ve arkasından 
 - username ve password ile 
 - user register olduğunda onu login yapmak istiyorsak şöyle bir algoritma kuarabiliriz. -> 
 - tabi django.contrib.auth dan authenticate ve login fonksiyonlarını da import etmeliyiz.
 
- Bu örnekte register olduktan sonra home page e yönlendirerek login yapmışız, ancak kullanıcı register olduğunda illa login olmak zorunda değil, login sayfasına da redirect edebiliriz ve kullanıcı orada username ve password girerek kendisi de login olabilir. 

 - Biz urls.py da login diye bir path belirlemedik ancak django.contrib.auth bize default olarak bir login view i ve urls i verdiği için biz o default login url inin name i olan login i kullanarak redirect login yapabiliyoruz.
  
```py
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password1")
        user=authenticate(username=username,password=password)
        login(request, user)
        return redirect('home')

```

user_example/views.py
```py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'user_example/index.html')

#! register -> login edip -> home page 
def register(request):
    form=UserCreationForm(request.POST or None)
    # form=UserCreationForm()
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        # username=form.cleaned_data["username"]
        # password=form.cleaned_data["password"]
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username = username, password = password)
        # return redirect('user_example:login')
        login(request, user)
        return redirect('user_example:home')
    context={
        "form": form,
    }
    return render(request, "registration/register.html", context)

```

###### urlpatterns'e app_name verme;
- DİKKAT!!!
- register ile user register ediliyor, fakat redirect ile yönlendirdiğimiz page'e gitmiyorsa eğer;
 - urls.py'da urlpatterns'nin hemen üzerinde app_name = 'name' şeklinde isimlendirme yapıp, redirect edeceğimiz page name'lerini de 'name:home' şeklinde yazmamız gerekiyor.

user_example/urls.py
```py
...

app_name = 'user_example'

urlpatterns = [
    ...
]
```

- Aynı şekilde settings.py'da ayarlamış olduğumuz redirect edilecek page'in formatı da şu şekilde olması gerekiyor.
 LOGIN_REDIRECT_URL = "user_example:home"

main/settings.py
```py
LOGIN_REDIRECT_URL = "user_example:home"
...
```



- Buraya kadar kullanıcı register olunca onu login ederek, home page'e yönlendiriyoruz.
- Eğer register olduktan sonra direkt home page'e girmesin dersek de login page'e yönlendirerek kendisinin login olmasını sağlayabiliriz.

- Aşağıda ise register view i ile bir kayıt işlemi yapan ve kayıt işlemi yaptıktan sonra login page e yönlendirilen user'ı görüyoruz. 

- Yukarıda da kayıt yaptıktan sonra username ve password ünü yakalayıp authentiacate ve login functions ları ile önce username ve password ekleyip otomatik olarak authenticate edip, sonra authenticate olmuş user ile login yapıp  home page yönlendiriyoruz.

- Register olduktan sonra django.contrib.auth un bize sağladığı login view ve url ile bizim hazırladığımız login template ine redirect yapılmış hali (hali hazırda biz login view ve url i yazmadık.);

user_example/views.py
```py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request, 'user_example/index.html')

#! register -> login page 
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(''user_example:login'')
    context={
        "form": form,
    }
    return render(request, 'registration/register.html', context)

```



##### Password_Change, Password_Change_Done

- password_change.html  oluşturacağız, django password_change için kendi administration sayfasında (accounts/password_change) kendi hazır template ine yönlendiriyor. 
- Biz bu template e yönlenmek istemiyoruz. Kendi template imizi koyup render etmek istiyoruz. 
- Ancak bu form ve view bizim için hazır biz sadece template ini kendimize göre değiştireceğiz.

- Biz password_change.html oluşturacağız, urls.py da 
```py
  from django.contrib.auth import views as auth_views
```   
import edip PasswordChangeView i çağırıp .as_view(template_name="registration/password_change.html")    şeklinde as_view içerisine kendi yazdığımız template i koyarak overrire edeceğiz. 
- Normalde bunun default u neymiş dokümandan bakarsak; default unun password_change_form.html olduğunu görürüz. Burada onu değiştiriyoruz. 
- Aslında bu işlemleri de yapmayabiliriz, sadece bir template (dokümanda geçen ismiyle yani register/password_change_form.html) ekleyerek de bu işlemleri yapabiliriz ancak önce bunu bi görelim sonra bu customization u yapmadan da bu password_change view ini gösterebiliriz ona da bakacağız.


- 1. Yöntem; urls.py da path ve import ettiğimiz PasswordChangeView'i kullanarak kendi custom "password_change" ve "password_change_done" template'imizi yazmak;
- Biz password_change için bir view yazmadık, urls.py da görüldüğü gibi auth.views deki PasswordChangeView ini alıp, onu customize ettik, as_view içerisindeki template name parametresini değiştirmişiz. (default olarak register/password_change_form.html olması gereken template ismini register/password_change.html olarak customize ettik.)

- Özetle djangonun bize otomatik default olarak verdiği password_change view inde customization yapmak istiyoruz, bunun default template ini değiştirmek istiyoruz ki bizi kendi template imize yönlendirsin.

- Burada kendimiz "password_change/" şeklinde custom bir end point belirleyebiliyoruz. Bu end pointe istek geldiğinde beni djangonun vermiş olduğu auth_views.PasswordChangeView ine yönlendir demişiz ama as_view in içerisine şunu yazarak -> template_name="registration/password_change.html" djangonun kullandığı default template yerine benim hazırladığım registration içerisindeki password_change.html i kullan demişiz. 

- Djangonun verdiği bütün view leri bu şekilde customize edebiliriz.

user_example/urls.py
```py
...
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"), name="password_change"),
]
```

- Şimdi registration içerisinde custom "password_change.html" oluşturuyoruz.

user_example/templates/registration/password_change.html
```html
<h1>Password Change</h1>

<form action="" method="post">

    {% csrf_token %}

    {{ form.as_p }}

    <input type="submit" value="Update">
    
</form>
```

- Evet artık biz djangonun bize vermiş olduğu "password_change" sayfasının (accounts/password_change/) yerine kendi template imizi render ediyoruz. Bu sayfaya erişebilmek için tabiki login olmamız gerekir. Eğer logout isek otomatik olarak login sayfasına yönlendiriyor.

- test ediyouz, "password_change/" ile password ümüzü değiştirebiliyoruz. Ancak hemen sonra django bizi "accounts/password_change/done/" isimli bir sayfaya yönlendirdi. Ancak biz zaten buraya yönlenmesini değil de kendi sayfamıza yönlendirilsin istiyoruz. 

- Peki bunu nasıl yapacağız? 
- registration klasörü altında dokümanda da belirtildiği isim "password_change_done.html" ile template oluşturursak eğer, password_change 'den sonra bizim oluşturduğumuz template render edilecektir. 

user_example/templates/registration/password_change_done.html
```html
<h1>Password change successful</h1>
<p>Your password was changed.</p>
<a href="{% url 'user_example:home' %}"><input type="submit" value="Home"></a>
```

- test ettik ama yine django kendi default password_change_done.html template'ini göstermeye çalışıyor, bizim customize ettiğimizi göstermiyor. Neden?
- django template'leri yukarıda itibaren okumaya başlıyor ve bizim yazdığımız custom template'ten önce aynı isimde kendi default template'ini bulunca onu render etmeye çalışıyor. Sıralamada geride kalıyoruz, settings.py da INSTALLED_APPS kısımında admin app'i en yukarıda olduğundan bu sorunla karşılaşıyoruz.  Bunu nasıl aşacağız?
- settings.py'da INSTALLED_APPS'de kendi user_app'imizi admin app'inin üzerine taşırsak aynı isimdeki template'lerden bizim yazdığımızı render edecektir. 

settings.py
```py
INSTALLED_APPS = [
    # myApps
    'user_example',
    'django.contrib.admin',
    ...
]
```

- test ettik, evet bu sefer başardık. Sonunda! Daha önceden de yaşamış olduğum sorun -> "accounts/" path'ini user app'imin urls.py'ına koymuş olmamdan kaynaklanıyormuş. Ama "accounts/" path'ini main/urls.py'ında tanımlayınca sorun çözüldü, normale döndü.



- 2. Yöntem; urls.py da path ve import ettiğimiz PasswordChangeView'i kullanmadan kendi custom "password_change" ve "password_change_done" template'imizi yazmak;
- Ya da sadece dokümanda geçtiği şekliyle yani;
 - "register/password_change_form.html" olarak registration klasörü altında bir html oluşturursak,
 - "register/password_change_done.html" olarak registration klasörü altında bir html oluşturursak,
 - Burada önemli olan husus template isimlerini değiştiremeyiz, dokümanda belirtildiği gibi kullanmalıyız.
 - yine, INSTALLED_APPS'deki user app'imizi, admin app'inin üzerine taşırsak,
 - urls.py'da PasswordChangeView'i render ederek template_name'ini değiştrmeye gerek kalmadan da 
 - kendi template'lerimizin render edilmesini sağlayabiliriz.

user_example/templates/registration/password_change_form.html
```html
<h1>Password Change</h1>

<form action="" method="post">

    {% csrf_token %}

    {{ form.as_p }}

    <input type="submit" value="Update">
    
</form>

```

user_example/templates/registration/password_change_done.html
```html
<h1>Password change successful</h1>
<p>Your password was changed.</p>
<a href="{% url 'user_example:home' %}"><input type="submit" value="Home"></a>

```

settings.py
```py
INSTALLED_APPS = [
    # myApps
    'user_example',
    'django.contrib.admin',
    ...
]
```

- Bundan sonra biz template'leri override ederken 2. yöntem üzerinden gideceğiz, 
- çünkü daha kolay, 
- app'imiz en üstte ve sadece kendi custom template'lerimize isim verirken djangonun default template'leriyle aynı isimde olmalarına dikkat edeceğiz o kadar.



##### Password Reset
- password_reset kullanabilmesi için user'ın aktif olması, login olmuş olması gerekir.
- django "/accounts/password_reset/" url'i ile bize default bir page sunuyor. Fakat biz bunu customize edeceğiz kendi page'imizi oluşturacağız.
- Biz app'imizi admin'in önüne aldığımız için, default template'in name'i (password_reset_form.html) ile aynı name'de olan kendi template'imizi oluşturup, djangonun bizimkini render etmesini sağlıyoruz.
- dokümanda yazdığı gibi default template name inde  "password_reset_form.html" oluşturuyoruz.

user_example/templates/registration/password_reset_form.html
```html
<h1>Password Reset</h1>

<form action="" method="post">

    {% csrf_token %}

    {{ form.as_p }}

    <input type="submit" value="Reset">
    
    <input type="hidden" value="{{ next }}" name="next">

</form>

```

- test ediyoruz, evet çalıştı. "/accounts/password_reset/" url'inden artık bizim custom template'imiz render ediliyor.

- Bundan sonra biz buraya mail adresimizi girdiğimiz zaman bize bir tane mail gönderecek, burada djangonun development için arkada set ettiği console backend diye bir email backend i var. Consolda bize email in bir dummy'sini gösteriyor.
  
###### Adjust a mail backend for development (Console backend):
    Geliştirme için bir posta arka ucunu ayarlayın

- Çalışan projede SMTP ayarları yapılarak gerçek zamanlı e-posta gönderimi ile sağlanıyor. Ancak development ortamında bu şekilde çalışılıyor.
 
(Instead of sending out real emails the console backend just writes the emails that would be sent to the standard output. By default, the console backend writes to stdout. You can use a different stream-like object by providing the stream keyword argument when constructing the connection.)

Konsol arka ucu, gerçek e-postalar göndermek yerine, standart çıktıya gönderilecek e-postaları yazar. Varsayılan olarak, konsol arka ucu stdout'a yazar. Bağlantıyı oluştururken akış anahtar sözcüğü argümanını sağlayarak akışa benzer farklı bir nesne kullanabilirsiniz.

(To specify this backend, put the following in your settings:)
Bu arka ucu belirtmek için settings.py a aşağıdakileri koyun:

```py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

- dokümandan console backend e gidiyoruz;
  
https://docs.djangoproject.com/en/4.1/topics/email/

şu ayarı settings.py a yazmamız gerekiyor:

<settings.py> ->

```py
# for password_reset email dummy;
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

```

- Bir de önemli olan husus password reset yapacak user ın kayıtlı e-mail inin olması gerekiyor. 

###### password_reset_done
- Artık "password_reset" template inde e postayı girip resete tıkladığımızda bizi yönlendirdiği sayfayı da dokümandan template ismi ile registration klasörü altında oluşturup kendi template imizi yazıyoruz;
  
user_example/templates/registration/password_reset_done.html
```html
<h1>Password reset sent</h1>
<p>We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.</p>

<p>If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder.</p>
```

###### password_reset_confirm
- consol umuza gelen dummy email ine tıkladığımızda default olarak gelen sayfayı da yine kendimizin oluşturduğu sayfaya yönlendirmek için default name i olan password_reset_confirm.html ile kendi template imizi yazıyoruz.
  
user_example/templates/registration/password_reset_confirm.html
```html
<h1>Password Reset Confirm Enter new password</h1>
<p>Please enter your new password twice so we can verify you typed it in correctly.</p>
<form action="" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Change my password">
</form>
```

###### password_reset_complete 
- password ümüzü yeniledikten sonra gelen sayfa ise default olarak password_reset_complete.html ve biz onun yerine aynı isimle kendimiz oluşturup aşağıdaki kodları yazıyoruz.
- login page'e yönlendiriyoruz.

user_example/templates/registration/password_reset_complete.html
```html
<h1>Password reset complete</h1>
<p>Your password has been set. You may go ahead and log in now.</p>
<a href="{% url 'login' %}">Login</a> 
```


##### login_required decorator Password Reset

- home page imizde bir if condition ile login olmuş olan yani authentiacate olmuş olan user farklı şeyler görebiliyor, login olmamış olan yani authentiacate olmamış olan user farklı şeyler görebiliyor.

- Ancak biz sadece login olmuş yani authentiacate olmuş userların görebileceği sayfalar olsun istiyorsak login required çok kullanışlı bir decorator. Mesela bir special.html diye bir template oluşturuyoruz. view ini ve url ini de belirtiyoruz.

- views.py da view ini yazıyoruz;

user-example/view.py
```py
def special(request):
    return render(request, 'user_example/special.html')
```

- urls.py da path ini tanımlıyoruz;

user-example/urls.py
```py
from .views import (
    ...
    special,
)

path('special/', special, name='special'),
```

- templates/user_example altında template ini yazıyoruz;

templates/user_example/special.html
```html
<h1>This is a special page!</h1>

<h3>Hello <span style="color:red;">{{ request.user }}!</span> You are lucky to see this page!</h3>
```

Şimdi yazdığımız bu sayfaya normal bir şekilde herkes girebiliyor. Ancak biz bu sayfaya gitmek isteyenlerin login olmasını istiyorsak login_required decoratorünü kullanarak bu sayfaya tıkladığında login sayfasına yönlendirilmesini sağlıyoruz. Bunun için views.py da şunu yazıyoruz; ->

- önce login_required import ediyoruz, arkasından render edilecek template imizin view inin başına @login_required yazıyoruz.

<views.py> ->

```py
from django.contrib.auth.decorators import login_required

@login_required
def special(request):
    return render(request, 'user_example/special.html')

```

- artık login değilken special.html page ine gitmeye çalıştığımızda bizi direct olarak login sayfasına yönlendiriyor.

- Buradaki fark home sayfasına login olan olmayan herkes girebiliyor, 
- Ancak içerik olarak login olan farklı içerik görüyor, olmayan farklı içerik görüyor. Burada ise login olmayan kimse sayfaya giremiyor.

- Bunun amacı sürekli views lerde user ın login olup olmadığını kontrol edilmesinin önüne geçen djangonun yazmış olduğu hazır bir decorator. 

- class_base view'lerde şöyle yapılıyor ->

views.py
```py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MyProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'my_protected_template.html'
```

settings.py.py
```py
# LOGOUT_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "user_example:home"
# LOGOUT_REDIRECT_URL = "home"
# LOGIN_URL = '/custom-login-url/'
```

##### Logout

- django default olarak bize LogoutView veriyor.
- Biz sadece logout olunca nereye redirect etmesi gerektiğini belirtmemizi bekliyor.
- Bunu da yine login ederken settings.py da LOGIN_REDIRECT_URL ile belirttiğimiz gibi, settings.py'da;
   LOGOUT_REDIRECT_URL = "/"
   LOGOUT_REDIRECT_URL = "user_example:home"
şeklinde belirtiyoruz.

settings.py
```py
# LOGOUT_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "user_example:home"
# LOGOUT_REDIRECT_URL = "home"
```

- Burada dikkat edilmesi gereken husus; logout işleminin loginden farklı olarak POST isteği ile yapılması, token gönderilmesi gerekiyor. Bu yüzden basit bir logout linki yeterli olmuyor. Bunun için form içinde csrf token ile Post isteği ile yapılması gerekiyor.

templates/index.html
```html 
...

<form method="POST" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>

...

```

- index.html de comments leri kaldırıp logout ve login linklerini aktif hale getirelim,







##### Linkleri sayfada uygun yerlerde tanımlayalım

###### register, add user link 
templates/index.html
```html 
...

<a href="{% url 'user_example:register' %}"><input type="submit" value="Register"></a> 

...

```

###### add password_change link/input 

- home page olan index.html'de login/authenticate olduktan sonra Password_Change butonu ile kendi yazdığımız  pasword_change_html template ine ulaşıp password change edelim.
  
templates/index.html
```html
<a href="{% url 'user_example:password_change' %}"><input type="submit" value="Password Change"></a>
```

- test ettik, password_change template'i ile password'ümüzü değiştirdik.


- Evet pasword ümüz değişti ve yine bizim hazırladığımız temp yani password_change_done geldi. Şimdi buraya bir link/button koyup home page e yönlendireceğiz. 

user-example/templates/registration/password_change_done.html
```html
<h1>Password change successful</h1>
<p>Your password was changed.</p>
<a href="{% url 'user_example:home' %}"><input type="submit" value="Home"></a>
```


###### add şifremi unuttum link/input 

- Şifremi unuttum. home page e şifremi unuttum link/button ile password_reset template ine yönlendirme -> 
  
- ilginçtir; ben direkt olarak home page olan index.html "pasword_reset" yazdım yine bizim hazırladığımız template geldi. Fakat bizim hazırladığımız template i override etmemiştik. template in ismi ise default olarak pasword_reset_form.html anlamadım???
- Şöyle oluyor; 
 - "accounts/password_reset/" url'inin name'i "password_reset"
 - bu isimle url çalıştırıldığında tetiklediği view'in template'i "password_reset_form.html"
 - biz de daha önceden kendi app'imizi admin app'inin önüne alarak default template yerine kendi yazdığımız ve default template ile aynı isimdeki "password_reset_form.html" render ediliyor.
  
<index.html> ->
```html
<a href="{% url 'password_reset' %}"><input type="submit" value="I forget my password"></a> 
```

------------------------------
- Bunu yani aşağıdaki işlemi yapmaya gerek yok!
- Ama biz yine prosedürü takip edip default template name ini değiştirip kendi template name imizi oluşturalım. Sadece name kısmını değiştiriyoruz.

<urls.py> ->
```py
    path('password_reset_form/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset_our_template"),
```

<index.html> ->
```html
<a href="{% url 'password_reset_our_template' %}"><input type="submit" value="I forget my password"></a> 
```
- Evet işte olu. Şimdi şifremizi değiştirelim... eposta girdim ve password resent sent mesajını aldım. Şimdi buradan login sayfasına link verelim mi?? Hayır çünkü epostaya gelen linke tıklaması gerekiyor.
------------------------------------

- Test edelim,
- Evet e-posta geldi, linke tıkladım ve Enter new password sayfası olan password_reset_confirm sayfası geldi, şifreyi değiştirdim ve password_reset_complete sayfası geldi ve orada login link/inputu var, onunla da login oldum.



###### special page (login required) için link verelim

- special page için index.html de link/button veriyoruz.

```html	
{% if user.is_authenticated %} 
<h1>
    Hello {{user.username | title}}    
</h1>

<a href="{% url 'user_example:special' %}"><input type="submit" value="Special"></a>
<a href="{% url 'logout' %}"><input type="submit" value="Logout"></a>
<a href="{% url 'password_change_our_template' %}"><input type="submit" value="Password Change"></a>


{% else %}
<h1>Hello, please login to see the page.</h1>

<a href="{% url 'user_example:special' %}"><input type="submit" value="Special"></a>
<a href="{% url 'login' %}"><input type="submit" value="Login"></a> 
<a href="{% url 'register' %}"><input type="submit" value="Register"></a> 
<a href="{% url 'password_reset_our_template' %}"><input type="submit" value="I forget my password"></a> 

{% endif %}
```


###### Links to official documentation

https://docs.djangoproject.com/en/4.1/topics/auth/default/

https://docs.djangoproject.com/en/4.1/ref/settings/

https://django-allauth.readthedocs.io/en/latest/overview.html

https://docs.djangoproject.com/en/4.1/topics/auth/customizing/





### Todo_App Ekleme

- Todo_App 'de ekstra kullanılmış olan paketleri yükleyip, INSTALLED_APPS'e ekliyoruz,
##### django-crispy-forms,  booststrap ile form styling

```bash
- pip install django-crispy-forms
- pip install crispy-bootstrap5
```

settings.py
```py
INSTALLED_APPS = [
    ...
    # third_party_packages
    'crispy_forms',
    "crispy_bootstrap5",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

```


- TodoApp settings ayarlarını yapalım,

settings.py
```py
INSTALLED_APPS = [
    ...
    # myApps
    'todo',
]
```

- todo urls name space ver


LOGIN_REDIRECT_URL = "todo:home"

Linkleri ayarla!
urls'lerdeki app_name'lere dikkat et!

