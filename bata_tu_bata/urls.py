"""bata_tu_bata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from boards import views

from accounts import views as accounts_views
from boards import views

urlpatterns = [

    # home boards
    url(r'^$', views.home, name='home'),
    
    # signup page
    url(r'^signup/$', accounts_views.signup, name='signup'),
    
    # login page
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    # logout status
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    
    # board topics
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    
    # creating a new topic
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    
    # admin url
    url(r'^admin/', admin.site.urls),

    # password reset urls
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_subject.txt'
            ),
        name='password_reset'
    ),
    url(r'^reset/done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    url(r'reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    )

]
