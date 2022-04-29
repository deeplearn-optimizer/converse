from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Tag, Project, Query
from django.contrib import messages
from .forms import ProjectForm, ReviewForm, QueryForm
#from .ai_util import *

from django.conf import settings
from django.core.mail import send_mail

from .utils import searchProjects, paginateProjects

def get_answer(request):
    s = " Person 1: Are there theatres in town? Person 2: There are 4 theatres in the center of town. Do you have a preference? Person 1: No, I don't have a preference. Which one do you recommend? Person 2: "
    #s = generate_dialogue(ReformerLM=model, model_state=STARTING_STATE, start_sentence=sample_sentence, vocab_file=VOCAB_FILE, vocab_dir=VOCAB_DIR, max_len=120, temperature=0.2)
    return HttpResponse(s)

def toggle_activation(request, pk):
    link = request.POST.get("link")
    query = Query.objects.get(id=pk)
    messages.success(request, 'Toggle operation completed successfully!')
    query.status = 'yes' if query.status == 'no' else 'no'
    query.save()

    subject = 'Your Bot is Active!'
    message = 'As a response to your query, we have activated your requested bot and you can eaily access it using this link\n'
    message += " " + link + " \n"
    message += " You can reply back this emil for any further assistance (if any)\n"
    message += " Thank you for choosing us and becoming our valuable customer"
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [query.owner.email],
        fail_silently = False,
    )
    print("called with link "+ link)

    return redirect('show_query', pk=query.id)
    
def show_query(request, pk):
    query = Query.objects.get(id=pk)
    return render(request, 'projects/query_info.html', {'query': query})

def queries(request):
    queries = Query.objects.all()
    context = {"queries" : queries}
    return render(request, 'projects/queries.html', context)

def query(request):
    form = QueryForm()
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.owner = request.user.profile
            query.save()

            messages.success(request, 'Query was successfully registered!')

            return redirect('projects')

        else:
            messages.error(
                request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'projects/query.html', context)


def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            context = {'form': form}
            return render(request, "projects/project_form.html", context)

    context = {'form': form}
    return render(request, "projects/project_form.html", context)

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})

