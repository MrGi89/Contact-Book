from .models import Person, Group


def people(request):

    all_people = Person.objects.all().order_by('last_name')

    return {
        'people': all_people,
    }

def groups(request):

    all_groups = Group.objects.all().order_by('name')
    return {
        'groups': all_groups,
    }
