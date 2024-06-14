from django.template import Template

from Category.models import Category

template = Template("My name is {{ my_name }}.")
def menu_links(request):
    all_categories= Category.objects.all()
    return dict(categories=all_categories)