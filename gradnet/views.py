from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import (Country, University, Program, Alumni, Service, Message, MyUser, Faq, ContactRequest, AlumniStory, Video)
from .forms import AlumniSignupForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
class ProgramListView(ListView):
    model = Program

    def get_context_data(self, **kwargs):
        context = super(ProgramListView, self).get_context_data(**kwargs)
        # TODO:: show only the programs that have at least one alumni in it.
        return context


class CountryListView(ListView):
    model = Country

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['object_list'] = Country.objects.filter(
            university__program__slug=self.kwargs['program_slug']
        ).distinct()
        context['program_slug'] = self.kwargs['program_slug']
        return context


class UniversityListView(ListView):
    model = University

    def get_context_data(self, **kwargs):
        context = super(UniversityListView, self).get_context_data(**kwargs)
        context['object_list'] = University.objects.filter(
            country__slug=self.kwargs['country_slug'], program__slug=self.kwargs['program_slug']
        )
        context['program_slug'] = self.kwargs['program_slug']
        context['country'] = Country.objects.get(slug__exact=self.kwargs['country_slug'])
        context['program'] = Program.objects.get(slug__exact=self.kwargs['program_slug'])
        return context


class AlumniListView(ListView):
    model = Alumni

    def get_context_data(self, **kwargs):
        context = super(AlumniListView, self).get_context_data(**kwargs)
        context['object_list'] = Alumni.objects.filter(
            university__slug=self.kwargs['university_slug'], program__slug=self.kwargs['program_slug']
        )
        context['university'] = University.objects.get(slug__exact=self.kwargs['university_slug'])
        return context


class AlumniDetailView(DetailView):
    model = Alumni

    def get_context_data(self, **kwargs):
        context = super(AlumniDetailView, self).get_context_data(**kwargs)
        return context


class AlumniSignUp(FormView):
    template_name = 'gradnet/alumni_signup.html'
    success_url = '/'
    model = Alumni
    form_class = AlumniSignupForm

    def form_valid(self, form):
        print("done")
        return super(AlumniSignUp, self).form_valid(form)


def login_view(request):

    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            # return render(request, 'gradnet/login.html', {'error_message': "logged in"})

            return HttpResponseRedirect('/')
        else:
            return render(request, 'gradnet/login.html', {'error_message': "Username/password isn't matching"})
            # return render(request=request, template_name='gradnet/login.html', context=error_message)
    else:
        return render(request, 'gradnet/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def alumni_dashboard(request):
    unread_messages = Message.objects.filter(seen=False, recipient=request.user.id)
    return render(request, 'gradnet/alumni_dashboard.html', {'unread_messages': unread_messages})


def services_view(request):
    services = Service.objects.all()
    return render(request, 'gradnet/services.html', {'services': services})


def services_per_alumni_view(request, slug):
    # TODO::JUST TAKE THIS ALUMNI'S SERVICE ONLY
    services = Service.objects.all()
    return render(request, 'gradnet/services_per_alumni.html', {'services': services})


def send_message_to_alumni(request, slug):
    if request.method == "POST":
        body = request.POST.get('message_body', '')
        alumni = Alumni.objects.filter(slug=slug).first()
        if alumni is not None:
            # Redirect to a success page.
            # return render(request, 'gradnet/login.html', {'error_message': "logged in"})
            print (body)
            message = Message(body=body, sender=request.user, recipient=alumni.user)
            message.save()
            return HttpResponseRedirect( request.path.replace("/message", ""))
        else:
            return HttpResponseRedirect(request.path.replace("/message", ""))
    else:
        return render(request, 'gradnet/message_to_alumni.html')


def faq_view(request):
    # query the database
    # save all the faq to a variable faq

    faqs = Faq.objects.filter(publish=True)
    return render(request, 'gradnet/faq.html', {'faqs': faqs})


def message_view(request):
    users = Message.objects.filter(recipient=request.user.id).order_by().values('sender').distinct()
    senders = []
    for user in users:
        x = MyUser.objects.get(id__exact=user['sender'])
        senders.append(x)

    selected_user = request.GET.get('user_id', '')
    if selected_user == '':
        return render(request, 'gradnet/message.html', {'senders': senders})

    if request.method == "POST":
        body = request.POST.get('message_body', '')
        recipient = MyUser.objects.get(id__exact = selected_user)
        if recipient is not None:
            # Redirect to a success page.
            # return render(request, 'gradnet/login.html', {'error_message': "logged in"})
            print (body)
            message = Message(body=body, sender=request.user, recipient=recipient)
            message.save()

            messages = Message.objects.filter(Q(sender=request.user.id, recipient_id=selected_user) | Q(sender=selected_user, recipient_id=request.user.id))
            return render(request, 'gradnet/message.html', {'senders': senders, 'messages': messages})
        else:
            messages = Message.objects.filter(Q(sender=request.user.id, recipient_id=selected_user) | Q(sender=selected_user, recipient_id=request.user.id))
            return render(request, 'gradnet/message.html', {'senders': senders, 'messages': messages})
    else:
        messages = Message.objects.filter(Q(sender=request.user.id, recipient_id=selected_user) | Q(sender=selected_user, recipient_id=request.user.id))
        return render(request, 'gradnet/message.html', {'senders': senders, 'messages': messages})


def student_dashboard(request):
    unread_messages = Message.objects.filter(seen=False, recipient=request.user.id)
    return render(request, 'gradnet/student_dashboard.html', {'unread_messages': unread_messages})


def about_view(request):
    return render(request, 'gradnet/about.html')


def roadmap_view(request):
    return render(request, 'gradnet/roadmap.html')


def contact_view(request):

    if request.method == "POST":
        body = request.POST.get('message_body', '')
        email = request.POST.get('email_id', '')

        print (body, email)
        cr = ContactRequest(body=body, email=email)
        cr.save()

        return render(request, 'gradnet/contact.html')

    else:
        return render(request, 'gradnet/contact.html')


class AlumniStoriesListView(ListView):
    model = AlumniStory

    def get_context_data(self, **kwargs):
        context = super(AlumniStoriesListView, self).get_context_data(**kwargs)
        context['object_list'] = AlumniStory.objects.filter(publish=True)
        return context


class AlumniStoryDetailView(DetailView):
    model = AlumniStory

    def get_context_data(self, **kwargs):
        context = super(AlumniStoryDetailView, self).get_context_data(**kwargs)
        return context


def videos_view(request):
    videos = Video.objects.filter(publish=True)
    return render(request, 'gradnet/videos.html', {'videos': videos})
