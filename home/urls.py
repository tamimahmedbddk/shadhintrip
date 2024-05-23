from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_tour_countries/', views.get_tour_countries, name='get_tour_countries'),
    path('get_tour_categories/', views.get_tour_categories, name='get_tour_categories'),
    path('get_tour_packages/', views.get_tour_packages, name='get_tour_packages'),
    path('get_visa_countries/', views.get_visa_countries, name='get_visa_countries'),
    path('get_visa_types/', views.get_visa_types, name='get_visa_types'),
    path('get_visa_packages/', views.get_visa_packages, name='get_visa_packages'),

    # site sections setting
    path("about", views.about_us, name="about-us"),
    path("privacy-policy", views.privacy_policy, name="privacy"),
    path("terms-of-service", views.terms_of_service, name="terms"),
    path("cancellation-policy", views.cancellation_policy, name="cancellation_policy"),
    path("refund-policy", views.refund_policy, name="refund_policy"),
    path("faq", views.faq, name="faq"),
]
