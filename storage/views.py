from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView


from .forms import LoginForm, RegisterForm, AddPersonForm, AddAddressForm, AddPhoneForm, AddEmailForm

from storage.models import Person, Address, Phone, Email, Group


class WelcomeView(View):

    def get(self, request):
        return render(request, template_name='welcome.html', context={})


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, template_name='user/register.html', context={'form': form})

    def post(self, request):

        # TODO - register site validation

        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            user_search = User.objects.filter(email=email)

            if password != password_confirmation:
                form.add_error('first_name', 'Passwords aren\'t equal')

            if user_search:
                form.add_error('email', 'This e-mail address is already taken')

            if form.has_error:
                return render(request, template_name='user/register.html', context={'form': form})
            else:
                return HttpResponse('zapisano')
        else:
            return HttpResponse('Nie podano wszytskich danych')


class LoginView(View):

    def get(self, request):

        form = LoginForm()
        return render(request, template_name='user/login.html', context={'form': form})

    def post(self, request):

        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_search = User.objects.filter(email=email)
            if user_search:
                user = authenticate(username=user_search[0].username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
        form.add_error('email', 'Email or password is incorrect. Please try again')
        return render(request, template_name='user/login.html', context={'form': form})


class AddPersonView(View):

    def get(self, request):

        form = AddPersonForm()
        return render(request, template_name='person/add_person.html', context={'form': form})

    def post(self, request):

        form = AddPersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            return HttpResponseRedirect(reverse('add_address', args=(person.id,)))

        form.add_error('first_name', 'Please fill in all the necessary fields')
        return render(request, template_name='person/add_person.html', context={'form': form})


class AddAddressView(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        form = AddAddressForm()
        return render(request, template_name='person/add_address.html', context={'form': form, 'person': person})

    def post(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        form = AddAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.person_address = person
            address.save()
            return HttpResponseRedirect(reverse('add_contacts', args=(person.id,)))

        form.add_error('city', 'Please fill in all the necessary fields')
        return render(request, template_name='person/add_address.html', context={'form': form, 'person': person})


class AddContactsView(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        phone_form = AddPhoneForm()
        email_form = AddEmailForm()
        return render(request, template_name='person/add_contacts.html', context={'phone_form': phone_form,
                                                                                  'email_form': email_form,
                                                                                  'person': person})

    def post(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        phone_form = AddPhoneForm(request.POST)
        email_form = AddEmailForm(request.POST)
        if phone_form.is_valid():
            number = phone_form.cleaned_data['number']
            number_type = phone_form.cleaned_data['number_type']
            if number and number_type:
                phone = phone_form.save(commit=False)
                phone.person_number = person
                phone.save()
            elif number and not number_type:
                phone_form.add_error('number', 'Please fill in all the necessary fields')

        if email_form.is_valid():
            address = email_form.cleaned_data['address']
            email_type = email_form.cleaned_data['email_type']

            if address and email_type:
                email = email_form.save(commit=False)
                email.person_email = person
                email.save()
            elif address and not email_type:
                email_form.add_error('address', 'Please fill in all the necessary fields')

        if email_form.has_error('address') or phone_form.has_error('number'):
            return render(request, template_name='person/add_contacts.html', context={'phone_form': phone_form,
                                                                                      'email_form': email_form,
                                                                                      'person': person})

        return HttpResponseRedirect(reverse('show_person', args=(person.id,)))


class ShowPeopleView(View):

    def get(self, request):

        return render(request, template_name='person/show_people.html', context={})


class ShowPersonView(View):

    def get(self, request, person_id):

        person = Person.objects.get(id=person_id)
        return render(request, template_name='person/show_person.html', context={'person': person})


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
            return redirect('/show/{}'.format(address.person_address.id))
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
        user_address = request.POST.get('address')
        email_type = int(request.POST.get('option'))
        if request.POST.get('action') == 'Change':
            if user_address:
                email.address = user_address
            email.email_type = email_type
            email.save()
            return redirect('/show/{}'.format(email.person_email.id))
        else:
            email.delete()
            return redirect('/show/{}'.format(email.person_email.id))


class ShowGroupsView(View):

    def get(self, request):

        groups = Group.objects.all().order_by('name')
        return render(request, template_name='group/show_groups.html', context={'groups': groups})

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Group.objects.create(name=name, description=description)
            return redirect('/groups/')
        else:
            return HttpResponse('Podaj dane')


class ShowGroup(View):

    def get(self, request, group_id):
        return render(request, 'show_group.html', {'groups': Group.objects.all().order_by('name'),
                                                   'group': Group.objects.get(id=int(group_id))})


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
