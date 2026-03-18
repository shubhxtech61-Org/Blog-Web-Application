from django.contrib import admin
from assignments.models import About, SocialLink

# for remove add button in admin panel
class AboutAdmin(admin.ModelAdmin):
  def has_add_permission(self, request):
    count = About.objects.all().count()
    if count == 0:
      return True
    return False
    
# Register your models here.
admin.site.register(About, AboutAdmin)
admin.site.register(SocialLink)