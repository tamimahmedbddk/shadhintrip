from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # site sections setting
    path("about", views.about_us, name="about-us"),
    path("privacy-policy", views.privacy_policy, name="privacy"),
    path("terms-of-service", views.terms_of_service, name="terms"),
    path("cancellation-policy", views.cancellation_policy, name="cancellation_policy"),
    path("refund-policy", views.refund_policy, name="refund_policy"),
    path("faq", views.faq, name="faq"),
]