from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('novel_index/', views.novel_index, name='novel_index'),
    path('novel_outline/', views.novel_outline, name='novel_outline'), 
    path('novel_keywords/', views.novel_keywords, name='novel_keywords'),
    path('handle_keyword_click/', views.novel_handle_keyword_click, name='handle_keyword_click'),
    path('keyword_confirmation/', views.novel_handle_keyword_confirmation, name='keyword_confirmation'),
    path('generate_questions/', views.novel_generate_questions, name='generate_questions'),
    path('seo_article/', views.seo_index, name='seo_index'),
    path('general_report/', views.report_index, name='report_index'),

]

