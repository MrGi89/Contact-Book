from django.shortcuts import render, redirect, Http404
from django.views import View

from storage.models import Person, Address, Phone, Email


class Home(View):

    def get(self, request):
        return render(request, 'home.html', {'people': Person.objects.all().order_by('last_name')})

    def post(self, request):
        if request.POST['option'] == 'edit':
            raise Http404


class AddPerson(View):

    def get(self, request):
        return render(request, 'add_person.html', {})

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        description = request.POST.get('description')

        if first_name and last_name:
            Person.objects.create(first_name=first_name, last_name=last_name, description=description)
            return redirect('/')
        else:
            raise Http404


class ShowPerson(View):

    def get(self, request, my_id):
        return render(request, 'show_person.html', {'person': Person.objects.get(id=int(my_id))})


class ModifyPerson(View):

    def get(self, request, my_id):
        return render(request, 'modify_person.html', {'person': Person.objects.get(id=int(my_id))})

    def post(self, request, my_id):
        person = Person.objects.get(id=int(my_id))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        description = request.POST.get('description')
        if first_name:
            person.first_name = first_name
        if last_name:
            person.last_name = last_name
        if description:
            person.description = description
        else:
            person.description = ''
        person.save()
        return redirect('/show/{}'.format(my_id))


class AddAddress(View):

    def post(self, request, my_id):
        person = Person.objects.get(id=int(my_id))
        city = request.POST.get('city')
        street = request.POST.get('street')
        number = request.POST.get('number')
        flat = request.POST.get('flat')

        if city and street and number and flat:
            try:
                (number, flat) = (int(number), int(flat))
                Address.objects.create(city=city, street=street, house_number=int(number)
                                       , flat_number=int(flat), person_address=person)
                return redirect('/show/{}'.format(my_id))
            except ValueError:
                return Http404('Podałeś błędne dane')
        elif city and street and number:
            try:
                number = int(number)
                Address.objects.create(city=city, street=street, house_number=int(number)
                                       , flat_number='', person_address=person)
                return redirect('/show/{}'.format(my_id))
            except ValueError:
                return Http404('Podałeś błędne dane')
        else:
            raise Http404('Nie podałeś żadnych danych')



class AddNumber(View):

    def get(self, request, my_id):
        pass


class AddEmail(View):

    def get(self, request, my_id):
        pass


class ModifyAddress(View):

    def get(self, request, my_id):
        pass


class ModifyNumber(View):

    def get(self, request, my_id):
        pass


class ModifyEmail(View):

    def get(self, request, my_id):
        pass


