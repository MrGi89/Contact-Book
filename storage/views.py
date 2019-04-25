from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView


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

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('show_people'))
        return render(request, template_name='user/register.html', context={'form': form})


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
                    return HttpResponseRedirect(reverse('show_people'))
        form.add_error('email', 'Email or password is incorrect. Please try again')
        return render(request, template_name='user/login.html', context={'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class AddPersonView(View):

    def get(self, request):

        form = AddPersonForm()
        return render(request, template_name='person/add_person.html', context={'form': form})

    def post(self, request):

        form = AddPersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            person.save()
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

    def get(self, request, pk):

        person = Person.objects.get(id=pk)
        return render(request, template_name='person/show_person.html', context={'person': person})


class UpdatePersonView(UpdateView):

    model = Person
    fields = ('first_name', 'last_name', 'description')
    template_name = 'person/update_person.html'
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        self.person_id = instance.id
        instance.save()

        return redirect(self.get_success_url(person_id=self.person_id))

    def get_success_url(self, **kwargs):
        person = Person.objects.get(pk=self.kwargs.get('pk'))
        if kwargs is not None:
            return reverse_lazy('show_person', kwargs={'person_id': person.id})


class EditPersonView(View):

    def get(self, request, pk):

        person = Person.objects.get(id=pk)
        return render(request, template_name='person/edit_person.html', context={'person': person})



class DeletePersonView(DeleteView):

    model = Person
    template_name = 'person/delete_person.html'
    success_url = reverse_lazy('show_people')


class ShowGroupsView(View):

    def get(self, request):

        return render(request, template_name='group/show_groups.html', context={})


class ShowGroupView(View):

    def get(self, request, group_id):

        group = Group.objects.get(pk=group_id)
        return render(request, 'group/show_group.html', {'group': group})


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


class AddToGroupsView(View):

    def get(self, request, person_id):
        person = Person.objects.get(pk=person_id)

        return render(request, template_name='person/add_to_groups.html', context={'person': person})


        # groups = Group.objects.all()
        # member = Person.objects.get(id=int(my_id)).group_set.all()
        # belong = []
        # not_belong = []
        # for group in groups:
        #     if group in member:
        #         belong.append(group)
        #     else:
        #         not_belong.append(group)
        # return render(request, 'person/add_to_groups.html', {'belong': belong, 'not_belong': not_belong})
        #
    # def post(self, request, my_id):
    #     member = Person.objects.get(id=int(my_id))
    #     groups = request.POST.getlist('group')
    #     if request.POST.get('action') == 'Add to group':
    #         if groups:
    #             for group in groups:
    #                 Group.objects.get(id=int(group)).members.add(member)
    #             return redirect('/')
    #         else:
    #             return HttpResponse('Nie zaznaczyłeś grupy')
    #     elif request.POST.get('action') == 'Add new group':
    #         return redirect('/groups')
    #
    #     return redirect('/')


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
