from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})

@login_required(login_url='login')
def post_question(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        return redirect('home')
    return render(request, 'post_question.html', {'form': form})

@login_required(login_url='login')
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all()
    form = AnswerForm(request.POST or None)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.user = request.user
        answer.question = question
        answer.save()
        return redirect('question_detail', question_id=question.id)
    return render(request, 'question_detail.html', {'question': question, 'answers': answers, 'form': form})

@login_required(login_url='login')
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    Like.objects.get_or_create(user=request.user, answer=answer)
    return redirect('question_detail', question_id=answer.question.id)
