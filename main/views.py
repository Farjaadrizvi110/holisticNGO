from django.views.generic import TemplateView, ListView, DetailView
from .models import Team, Blog

# Static Pages
class HomePageView(TemplateView):
    # Specify which HTML template this view will render
    template_name = 'index.html'

    # Override the method that prepares data to be passed to the template
    def get_context_data(self, **kwargs):
        # Step 1: Get the existing context from the base class
        context = super().get_context_data(**kwargs)

        # Step 2: Query the Blog model to get all blog posts, ordered by latest created
        # This fetches all instances of the Blog model from the database and orders them by creation date in descending order.
        all_blogs = Blog.objects.all().order_by('-created_at')

        # Step 3: Add this list of blogs to the context dictionary under a meaningful key
        context['blogs'] = all_blogs

        # Step 4: Return the enriched context to be used in rendering the template
        return context

class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_members = Team.objects.all()
        context['team_members'] = team_members
        return context

class ServicesPageView(TemplateView):
    template_name = 'services.html'

class TestimonialsPageView(TemplateView):
    template_name = 'testimonials.html'

class ContactPageView(TemplateView):
    template_name = 'contact.html'

class DonationPageView(TemplateView):
    template_name = 'donation.html'

class FAQsPageView(TemplateView):
    template_name = 'faqs.html'

# Dynamic Data-Driven Pages
class TeamListView(TemplateView):
    template_name = 'team.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_members = Team.objects.all()
        context['team_members'] = team_members
        return context

class BlogListView(TemplateView):
    template_name = 'blog.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_blogs = Blog.objects.all().order_by('-created_at')
        context['blogs'] = all_blogs
        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog-single.html'
    context_object_name = 'blog'
