

from assignments.models import SocialLink
from blogs.models import category


def get_categories(request):
  categories = category.objects.all()
  return dict(categories=categories)


def get_social_links(requests):
  social_links = SocialLink.objects.all()
  return dict(social_links=social_links)