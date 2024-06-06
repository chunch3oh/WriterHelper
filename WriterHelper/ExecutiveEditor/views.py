from django.shortcuts import render, redirect
from .forms import InputForm
from . import FunctionOfSQLite as fsql
from . import FunctionOfLLM as llm
import random

api_key = "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"
organization = 'org-RDVlX0EpMMkd3ejDxtoGdKoZ'
NameOfDB='Books'
WorkingChapter="CH1"

def index(request):
    return render(request, 'index.html')

def novel_index(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            field1 = form.cleaned_data['field1']
            field2 = form.cleaned_data['field2']
            field3 = form.cleaned_data['field3']
            field4 = form.cleaned_data['field4']

            request.session['field1'] = field1
            request.session['field2'] = field2
            request.session['field3'] = field3
            request.session['field4'] = field4
            
            return redirect('novel_outline')
    else:
        form = InputForm()
    return render(request, 'novel_index.html', {'form': form})

def seo_index(request):
    return render(request, 'seo_index.html')

def report_index(request):
    return render(request, 'report_index.html')


def novel_outline(request):
    DefaultStyle=["奇幻","科幻","愛情","熱血"]
    DefaultTime=["中古世紀","未來","現代","爸媽年代"]
    DefaultPlace=["城堡","外太空","校園","大明湖畔"]
    Style = request.session.get('field1') or random.choice(DefaultStyle)
    Time = request.session.get('field2') or random.choice(DefaultTime)
    Place = request.session.get('field3') or random.choice(DefaultPlace)
    OtherInformation = request.session.get('field4') or " "
    outline = llm.GenerateOutline(Style,Time,Place,OtherInformation)
    if request.method == 'POST':
        if 'try_another' in request.POST:  
            outline = llm.GenerateOutline(Style,Time,Place,OtherInformation)
        elif 'confirm' in request.POST:  
            Column=['Title', 'Introduction', 'Characters','CH1']
            Content=['曲終人散：林黛玉與佛地魔的交錯','一場跨越時空和文化的奇異相遇，紅樓夢中的林黛玉與哈利波特世界的佛地魔，他們的相遇將激起怎樣的波瀾？這場將現實與魔法交織的故事，將如何改變他們的命運？','林黛玉，紅樓一夢中的才女，智慧、機敏與美麗的象徵；佛地魔，一個追求不朽、權力至上的黑巫師，以無情和狡猾著稱。','故事從格林德沃在阿兹卡班的囚籠中接到佛地魔的求見信開始，他對這場會面的預感和疑慮充斥著他的心中。此時，讀者透過格林德沃的內心獨白，對兩個角色的背景和矛盾有了初步的理解。']
            fsql.Building(NameOfDB, Column,Content)
            return redirect('novel_keywords')


    return render(request, 'novel_outline.html', {'outline': outline})

def novel_keywords(request):
    print("====novel_keywords====\n")
    outline = fsql.TakeContent(NameOfDB, WorkingChapter)
    keywords = llm.GenerateKeyWords(api_key, organization, outline)
    return render(request, 'novel_keywords.html', {'keywords': keywords})

def novel_handle_keyword_click(request):
    print("====novel_handle_keyword_clicks====\n")
    if request.method == 'POST':
        clicked_keyword = request.POST.get('keyword')
        request.session['clicked_keyword'] = clicked_keyword

    return redirect('novel_keyword_confirmation')

def novel_handle_keyword_confirmation(request):
    print("====novel_handle_keyword_clicks====\n")
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')
        if confirmation == 'Yes':
            clicked_keyword = request.session.get('clicked_keyword')
            return redirect('novel_generate_questions')  
        else:
            return redirect('novel_keywords')  

    return redirect('novel_generate_questions') 

def novel_generate_questions(request):
    Keywordschosen = request.session.get('clicked_keyword')
    print(type(Keywordschosen))
    print(Keywordschosen)
    Questions=llm.GenerateQuestions(api_key,organization,Keywordschosen,NameOfDB,WorkingChapter)
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if str(answer)<30:
            answer=llm.Expand(api_key,organization,answer,Questions)
        request.session['answer'] = answer
        return redirect('novel_new_outline')

    return render(request, 'novel_generate_questions.html', {'Questions': Questions})

