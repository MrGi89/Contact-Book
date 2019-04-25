from django.contrib.auth.models import User

from .models import Person, Group


def people(request):

    users = User.objects.all()
    if request.user in users:
        all_people = Person.objects.filter(user=request.user).order_by('last_name')
        return {'people': all_people, }
    return {}


def groups(request):

    users = User.objects.all()
    if request.user in users:
        all_groups = Group.objects.filter(user=request.user).order_by('name')
        return {'groups': all_groups, }
    return {}
