from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from .forms import *
from .models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')
def user_home(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')

        attempted_question = profile.attempts.select_related('question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect('submission-result', attempted_question_pk = attempted_question.id )

    else:
        question = profile.get_new_question()
        if question is not None:
            profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'user-home.html', context=context)
def leaderboard(request):
    top_profiles = Profile.objects.order_by('-total_score')
    return render(request, 'leaderboard.html', {'top_profiles':top_profiles})
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    return render(request, 'submission-result.html', {'attempted_question':attempted_question})
def login(request):

    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('user-home')
        else:

            return redirect('login')
       
    return render(request, 'login.html', {'form':form})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})

def logout(request):
    auth.logout(request)
    return redirect('home')

