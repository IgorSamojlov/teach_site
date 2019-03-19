from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choise

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = {
#        'latest_question_list':latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
GET /users - index user
GET /users/:id - show user
POST /users - create new user
PUT /users/:id - udpate exiting user
DELTE /users/:id - destroy user

GET /users/new - render user new form
GET /users/:id/edit - render edit existing user form

"""


def vote (request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choise_set.get(pk=request.POST['choice'])
    except (KeyError, Choise.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question':question,
                'error_message': 'You didnt selected choice'
                })

    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse(
            'polls:results', args=(question.id,)))

