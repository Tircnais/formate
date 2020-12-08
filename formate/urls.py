"""formate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# include para agregar las URLS de las app
from django.urls import path, include
# Para los archivos estaticos
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views

# PAra el manejor de error personalizados
from django.conf.urls import handler404, handler500
from dashboard.errorHandling import *
# handler400 = 'dashboard.errorHandling.bad_request' #si hay
# handler401 = 'dashboard.errorHandling.no_autorizado'
# handler403 = 'dashboard.errorHandling.permission_denied' #si hay
handler404 = 'dashboard.errorHandling.no_encontrada' #si hay
handler500 = 'dashboard.errorHandling.server_error'#si hay


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls'), name='appPanel'),
    path('buscador/', include('buscador.urls'), name='appBuscador'),
    # path('modelofastText/', include('prediccion.urls'), name='appPrediccion'),
    path('api_rest/', include('api_rest.urls'), name='api-rest'),
    # Usuarios create
    path('accounts/', include('django.contrib.auth.urls')),
    # iniciar seccion
    path('accounts/login/', views.LoginView.as_view(template_name ='registration/login.html'), name='login'),
    # cerrar seccion
    path('accounts/logout/', views.LogoutView.as_view(template_name = 'registration/logout.html'), name='logout'),
    # Cambiar clave de usuario
    path('accounts/password_change/', views.PasswordChangeView.as_view(template_name = 'registration/password_change_form.html'), name='password_change'),
    path('accounts/password_change/done/', views.PasswordChangeDoneView.as_view(template_name ='registration/password_change_done.html'), name='password_change_done'),
    # restablecer calve (vista y el templeta para el EMAIL literal)
    path('accounts/password_reset', views.PasswordResetView.as_view(template_name ='registration/password_reset_form.html', email_template_name = 'registration/password_reset_email.html'), name='password_reset'),
    path('accounts/password_reset/done/', views.PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html'), name='password_reset_done'),
    #A donde nos lleva ras recuperar la registration
    path('accounts/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name = 'registration/password_reset_confirm.html'), name='password_reset_confirm'),
    #Mensaje que nos mostraria el reseteo de la registration y luego el LOGIN
    path('accounts/reset/done/', views.PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)