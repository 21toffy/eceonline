from django.urls.conf import path
from QA import views
from .views import SearchResultsView

app_name = 'QA'

urlpatterns = [
    
    path('', views.TodaysQuestionList.as_view(), name='daily_question'),
    path('ask', views.about, name='about'),
    path('home/ask', views.AskQuestionView.as_view(), name='ask'),
    #dont forget that you will need to change the url pattern from 'q/<int:pk>', to 'question/<int:pk>',
    path('QA/home/q/<int:pk>', views.QuestionDetailView.as_view(), name='question_detail'),
    path('QA/home/q/<int:pk>/answer', views.CreateAnswerView.as_view(), name='answer_question'),
    path('QA/home/a/<int:pk>/accept', views.UpdateAnswerAcceptanceView.as_view(), name='update_answer_acceptance'),
    path('QA/home/daily/<int:year>/<int:month>/<int:day>/', views.DailyQuestionList.as_view(), name='daily_questions'),
    path('QA/home/q/unanswered/', views.NoAnswer, name='NoAnswer'),
    path('QA/home/q/unanswered/<int:pk>', views.NoAnswerdetail, name='No_answer_detail'),
    path('QA/home/q/search', views.SearchResultsView, name='search_results'),

    path('search/', views.post_search, name='post_search'),

]


