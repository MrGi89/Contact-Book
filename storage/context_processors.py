from .models import Person


def people(request):

    all_people = Person.objects.all().order_by('last_name')

    return {
        'people': all_people,
    }
