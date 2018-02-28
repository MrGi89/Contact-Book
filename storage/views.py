from django.shortcuts import render, redirect, Http404, HttpResponse
from django.views import View

from storage.models import Person, Address, Phone, Email, Group


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
            person = Person.objects.create(first_name=first_name, last_name=last_name, description=description)
            return redirect('/show/{}'.format(person.id))
        else:
            return HttpResponse('Podałes błędne dane')


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
        if request.POST.get('submit') == 'change':
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
        else:
            person.delete()
            return redirect('/show/{}'.format(my_id))


class DeletePerson(View):

    def get(self, request, my_id):
        person = Person.objects.get(id=int(my_id))
        person.delete()
        return redirect('/')
        

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
                Address.objects.create(city=city, street=street, house_number=number
                                       , flat_number=flat, person_address=person)
                return redirect('/show/{}'.format(my_id))
            except ValueError:
                return HttpResponse('Podałeś błędne dane')
        elif city and street and number:
            try:
                number = int(number)
                Address.objects.create(city=city, street=street, house_number=number
                                       , person_address=person)
                return redirect('/show/{}'.format(my_id))
            except ValueError:
                return HttpResponse('Podałeś błędne dane')
        else:
            return HttpResponse('Nie podałeś żadnych danych')


class AddNumber(View):

    def post(self, request, my_id):
        person = Person.objects.get(id=int(my_id))
        number = request.POST.get('number')
        number_type = request.POST.get('option')
        if number:
            try:
                number = int(number)
                Phone.objects.create(number=number, number_type=int(number_type), person_number=person)
                return redirect('/show/{}'.format(my_id))
            except ValueError:
                return HttpResponse('Podałeś błędne dane')
        else:
            return HttpResponse('Nie podałeś żadnych danych')


class AddEmail(View):

    def post(self, request, my_id):
        person = Person.objects.get(id=int(my_id))
        email = request.POST.get('email')
        email_type = request.POST.get('option')
        if email:
            Email.objects.create(address=email, email_type=int(email_type), person_email=person)
            return redirect('/show/{}'.format(my_id))
        else:
            return HttpResponse('Nie podałeś żadnych danych')


class ModifyAddress(View):

    def post(self, request, my_id):
        address = Address.objects.get(id=int(my_id))
        city = request.POST.get('city')
        street = request.POST.get('street')
        house_number = request.POST.get('house_number')
        flat_number = request.POST.get('flat_number')
        if request.POST.get('action') == 'Change':
            if house_number:
                try:
                    house_number = int(house_number)
                    address.house_number = house_number
                except ValueError:
                    return HttpResponse('Błędne dane')
            if flat_number:
                try:
                    flat_number = int(flat_number)
                    address.flat_number = flat_number
                except ValueError:
                    return HttpResponse('Błędne dane')
            else:
                address.flat_number = None
            if city:
                address.city = city
            if street:
                address.street = street
            address.save()
            return redirect('/show/{}'.format(address.person_address))
        else:
            address.delete()
            return redirect('/show/{}'.format(address.person_address.id))


class ModifyNumber(View):

    def post(self, request, my_id):
        phone = Phone.objects.get(id=int(my_id))
        user_number = request.POST.get('number')
        number_type = request.POST.get('option')

        if request.POST.get('action') == 'Change':
            try:
                if user_number:
                    user_number = int(user_number)
                    phone.number = user_number
                phone.number_type = int(number_type)
                phone.save()
                return redirect('/show/{}'.format(phone.person_number.id))
            except ValueError:
                return HttpResponse('Podałeś błędne dane')
        else:
            phone.delete()
            return redirect('/show/{}'.format(phone.person_number.id))


class ModifyEmail(View):

    def post(self, request, my_id):
        email = Email.objects.get(id=int(my_id))
        address = request.POST.get('address')
        email_type = request.POST.get('option')

        if request.POST.get('action') == 'Change':
            if address:
                email.address = email
            address.email_type = int(email_type)
            return redirect('/show/{}'.format(email.person_email.id))
        else:
            email.delete()
            return redirect('/show/{}'.format(email.person_email.id))


class ShowGroups(View):

    def get(self, request):
        return render(request, 'show_groups.html', {'groups': Group.objects.all().order_by('name')})

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Group.objects.create(name=name, description=description)
            return redirect('/groups/')
        else:
            return HttpResponse('Podaj dane')


class AddMembers(View):

    def get(self, request, my_id):
        people = Person.objects.all()
        members = Group.objects.get(id=int(my_id)).members.all()
        belong = []
        not_belong = []
        for person in people:
            if person in members:
                belong.append(person)
            else:
                not_belong.append(person)
        return render(request, 'add_members.html', {'belong': belong, 'not_belong': not_belong})

    def post(self, request, my_id):
        group = Group.objects.get(id=int(my_id))
        members = request.POST.getlist('member')
        if request.POST.get('action') == 'Add':
            if members:
                for member in members:
                    group.members.add(Person.objects.get(id=int(member)))
                return redirect('/groups')
            else:
                return HttpResponse('Nie zaznaczyłeś użytkownika')
        return redirect('/groups')


class AddToGroups(View):

    def get(self, request, my_id):
        groups = Group.objects.all()
        member = Person.objects.get(id=int(my_id)).group_set.all()
        belong = []
        not_belong = []
        for group in groups:
            if group in member:
                belong.append(group)
            else:
                not_belong.append(group)
        return render(request, 'add_to_groups.html', {'belong': belong, 'not_belong': not_belong})

    def post(self, request, my_id):
        member = Person.objects.get(id=int(my_id))
        groups = request.POST.getlist('group')
        if request.POST.get('action') == 'Add to group':
            if groups:
                for group in groups:
                    Group.objects.get(id=int(group)).members.add(member)
                return redirect('/')
            else:
                return HttpResponse('Nie zaznaczyłeś grupy')
        elif request.POST.get('action') == 'Add new group':
            return redirect('/groups')

        return redirect('/')


class DeleteMember(View):

    def get(self, request, group_id, member_id):
        Group.objects.get(id=int(group_id)).members.remove(Person.objects.get(id=int(member_id)))
        return redirect('/groups')


class ModifyGroup(View):

    def get(self, request, group_id):
        return render(request, 'modify_group.html', {'group': Group.objects.get(id=int(group_id))})

    def post(self, request, group_id):
        group = Group.objects.get(id=int(group_id))
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            group.name = name
        if description:
            group.description = description
        else:
            group.description = ''
        group.save()
        return redirect('/groups')


class DeleteGroup(View):

    def get(self, request, group_id):
        Group.objects.get(id=int(group_id)).delete()
        return redirect('/groups')
