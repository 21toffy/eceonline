from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404, HttpResponse

from django.shortcuts import render, redirect


from django.views import generic
from django.views.generic import CreateView, DetailView, UpdateView, DayArchiveView, RedirectView, ListView
from QA.forms import QuestionForm, AnswerForm, AnswerAcceptanceForm, SearchForm
from QA.models import Question, Answer
from django.urls.base import reverse
from django.utils import timezone
from django.shortcuts import render

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank




def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Question.objects.annotate(search=SearchVector('title', 'question'),).filter(search=query)
    return render(request, 'QA/search_results.html', {'form': form, 'query': query, 'results': results})




def NoAnswer(request):
    qs = Question.objects.all()
    nakedquestions = qs.filter(answers__isnull=True)
    context = {'nakedquestions':nakedquestions}
    template_name = 'QA/unanswered.html'
    return render(request,template_name,context)

def about(request):
    template_name = 'QA/about.html'
    return render(request, template_name)


class SearchResultsView(ListView):
    model = Question
    template_name = 'search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Question.objects.filter(
            Q(title__icontains=query) | Q(question__icontains=query)
        )
        return object_list



def NoAnswerdetail(request, pk):
    try:
        not_answered= Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        raise Http404('does not exist ')

    return render(request, 'QA/noanswerdetail.html', {'not_answered': not_answered})





class DailyQuestionList(DayArchiveView):
    queryset = Question.objects.all()
    date_field = 'created'
    month_format = '%m'
    allow_empty = True

class TodaysQuestionList(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        today = timezone.now()
        return reverse(
            'questions:daily_questions',
            kwargs={
                'day': today.day,
                'month': today.month,
                'year': today.year,
            }
        )



'''view that handles question asking'''

class AskQuestionView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'QA/ask.html'
    def get_initial(self):
        return {'user': self.request.user.id}

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            preview = Question(
                question=form.cleaned_data['question'],
                title=form.cleaned_data['title'])
            ctx = self.get_context_data(preview=preview)
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()

#view that handles details of a quesion

class QuestionDetailView(DetailView):
    model = Question

    ACCEPT_FORM = AnswerAcceptanceForm(initial={'accepted': True})
    REJECT_FORM = AnswerAcceptanceForm(initial={'accepted': False})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'answer_form': AnswerForm(initial={
                'user': self.request.user.id,
                'question': self.object.id,
            })
        })
        if self.object.can_accept_answers(self.request.user):
            ctx.update({
                'accept_form': self.ACCEPT_FORM,
                'reject_form': self.REJECT_FORM,
            })
        return ctx



class CreateAnswerView(LoginRequiredMixin, CreateView):
    form_class = AnswerForm
    template_name = 'QA/create_answer.html'

    def get_initial(self):
        return {
            'question': self.get_question().id,
            'user': self.request.user.id,
        }

    def get_context_data(self, **kwargs):
        return super().get_context_data(question=self.get_question(), **kwargs)

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'SAVE':
            # save and redirect as usual.
            return super().form_valid(form)
        elif action == 'PREVIEW':
            ctx = self.get_context_data(preview=form.cleaned_data['answer'])
            return self.render_to_response(context=ctx)
        return HttpResponseBadRequest()

    def get_question(self):
        return Question.objects.get(pk=self.kwargs['pk'])

class UpdateAnswerAcceptanceView(LoginRequiredMixin, UpdateView):
    form_class = AnswerAcceptanceForm
    queryset = Answer.objects.all()

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_invalid(self, form):
        return HttpResponseRedirect(
            redirect_to=self.object.question.get_absolute_url())
