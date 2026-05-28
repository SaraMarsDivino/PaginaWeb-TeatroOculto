from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_view, name='root'),
    path('skip-intro/', views.skip_intro_view, name='skip_intro'),
    path('newsletter/', views.newsletter_subscribe_view, name='newsletter_subscribe'),
    path('listas/', views.listas_view, name='listas'),
    path('mensajes/', views.mensajes_view, name='mensajes'),
    path('inicio/', views.home_view, name='home'),
    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('iniciativas/', views.iniciativas_view, name='iniciativas'),
    path('obras/', views.obras_view, name='obras'),
    path('contacto/', views.contacto_view, name='contacto'),
]
