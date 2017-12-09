from django.conf import settings
from django.conf.urls import include, url
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from home.views import *
from django.contrib import admin
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm,password_reset_complete,logout
from django.contrib.auth.forms import PasswordResetForm
admin.autodiscover()

urlpatterns = [
    url(r'^unsubscribe/$', login_required(Unsubscribe), name="unsubscribe"),
    url(r'^support/$', staff_member_required(Support),  name="support"),
    url(r'^logout/$', logout, {'next_page': '/'}, name="logout_page"),
    url(r'^signup/$', SignupView, name='signup_page'),
    url(r'^signup/premium/$', SignupViewPremium, name='signup_page_premium'),
    url(r'^signup/ministerial/$', SignupViewMinisterial, name='signup_page_ministerial'),
    url(r'^signup/email_sent/(?P<email>.{1,254})$', SignupEmailSentView.as_view(), name='signup_email_sent_page'),
    url(r'^signup/verify/yes/$', SignupVerified.as_view(), name='signup_verified_page'),
    url(r'^signup/verify/not/$', SignupNotVerified.as_view(), name='signup_not_verified_page'),
    url(r'^signup/verify/$', SignupVerifyView.as_view(), name='signup_verify'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login_page'),
    url(r'^password/reset/$', password_reset,{'template_name':'home_password_reset.html',
                                              'email_template_name':'email/home_reset_password.txt',
                                              'html_email_template_name':'email/home_reset_password.html',
                                              'subject_template_name':'email/home_reset_password_subject.txt',
                                              'password_reset_form': PasswordResetForm,
                                              'from_email': settings.EMAIL_HOST_USER,
                                              }, name='password_reset_page'),
    url(r'^password/reset/done/$', password_reset_done,{'template_name':'home_password_reset_email_sent.html'},name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': 'home_password_reset_verified.html'}, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'home_password_reset_success.html'},
        name='password_reset_complete'),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'home/$',staff_member_required(Home.as_view()),name='home'),
    url(r'juan/ballistreri/$',JuanBallistreri,name='juan_ballistreri'),
    url(r'panel/$',login_required(PanelUsuario),name='home_panel'),
    url(r'usuarios/$',staff_member_required(Usuarios),name='home_usuarios'),
    url(r'blog/$',TemplateView.as_view(template_name='en_construccion.html'),name='home_blog')

]
