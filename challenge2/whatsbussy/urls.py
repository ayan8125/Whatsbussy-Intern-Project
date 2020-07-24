"""whatsbussy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from subcriptions import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/signup/', views.signup, name='signup'),

    path('SIGNUP/', views.SIGNUP, name='SIGNUP'),
    path('Login/', views.Login, name='Login'),
    path('user/login/', views.logins, name='login_ajax'),
    path('LOGOUT/', views.LOGOUT, name='LOGOUT'),
    path('success/session_id=<str:CHECKOUT_SESSION_ID>/',
         views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('subscription_webhooks/', views.subscription_webhook,
         name='subscription_webhook'),
    path('Premiunm/', views.Premiunm, name='Premiunm'),
    path('subscriptionofPremiunm/', views.subscriptionofPremiunm,
         name='subscriptionofPremiunm'),
    path('makesubscription/Premier/',
         views.makesubscription, name="makesubscription"),
    path('Basic/', views.Basic, name='Basic'),
    path('makebasicsubscription/', views.makebasicsubscription,
         name='makebasicsubscription'),
    path('MySubscription/', views.MySubscription, name='MySubscription'),
    path('cancelmysubscription/', views.cancel_mysubscription,
         name='cancelmysubscription'),
    path('admin/', admin.site.urls),
]
