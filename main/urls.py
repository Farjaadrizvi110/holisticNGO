from django.urls import path
from .views import (
    HomePageView, AboutPageView, ServicesPageView, TestimonialsPageView,
    ContactPageView, DonationPageView, FAQsPageView,
    TeamListView, BlogListView, BlogDetailView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('services/', ServicesPageView.as_view(), name='services'),
    path('testimonials/', TestimonialsPageView.as_view(), name='testimonials'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('donation/', DonationPageView.as_view(), name='donation'),
    path('faqs/', FAQsPageView.as_view(), name='faqs'),
    path('team/', TeamListView.as_view(), name='team'),
    path('blogs/', BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
