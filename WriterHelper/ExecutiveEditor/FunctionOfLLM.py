import openai
import random
import csv
import os
import re
from . import FunctionOfSQLite as fsql

def GenerateOutline(Style,Time,Place,OtherInformation):
    num = random.randint(1, 100)
    outline="outline"+str(num)
    return outline
    
def Expand(api_key,organization,Reply,QD):
    openai.api_key = api_key
    openai.organization = organization
    p="Here's a sentence:\n" + Reply +"\nPlease make it more coherent according to the following questions or details:\n" + QD + "\nYou should reply in Traditional Chinese and follow this template :\n R:\n"
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p}
        ]
    )
    
    print(chat.choices[0].message['content'])
    
    x=chat.choices[0].message['content'].split('R:')
    
    return x[1]

def GenerateKeyWords(api_key,organization,outline):
    openai.api_key = api_key
    openai.organization = organization
    p="please generate few key words includes: 人、事、時、地、物 and based on the following article. If there's nothing is matched then just print 無, also, if there's more than 2 items then use ',' to seperate them. Your output should follow this template\n人:\n事:\n時:\n地:\n物:\n, please show the result in Traditional Chinese :\n"+outline   
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p}
        ]
    )
    
    print(chat.choices[0].message['content'])
    
    x=chat.choices[0].message['content'].split('\n')
    tmp=[]

    for i in range(len(x)) :
        tmp.append(re.split(': |：', x[i]))

    KeyWords=[]
    KeyWords.append(tmp[0][1].split(','))
    KeyWords.append(tmp[1][1].split(','))
    KeyWords.append(tmp[2][1].split(','))
    KeyWords.append(tmp[3][1].split(','))
    KeyWords.append(tmp[4][1].split(','))

    return KeyWords

def GenerateQuestions(api_key,organization,KeyWordsChosen,NameOfDB,WorkingChapter):
    openai.api_key = api_key
    openai.organization = organization
    content = fsql.TakeContent(NameOfDB, WorkingChapter)
    p = "Here is the original outline of the article :\n"+content+"\nPlease give me 3 questions related to " + KeyWordsChosen +"that added can make the article more complete and intriguing. Those questions should follow the template:\nQ.\nQ.\nQ.\n Please show in Traditional Chinese only" 
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p}
        ]
    )
    print("start print response\n",chat.choices[0].message['content'])
    x=chat.choices[0].message['content'].split('\n')
    tmp=[]
    for i in range(len(x)) :
        tmp.append(x[i].split('. '))

    Questions=[]
    for i in range(len(tmp)):
        if(len(tmp[i])>1):
            Questions.append(tmp[i][1])

    return Questions

def MergeOutlineByQuestions(api_key,organization,Reply,NameOfDB,WorkingChapter):
    openai.api_key = api_key
    openai.organization = organization
    content = fsql.TakeContent(NameOfDB, WorkingChapter)
    p = "Here is the original outline of the article :\n"+content+"\nAlso, here is some reply that we think that can make the outline better\n" + Reply + "\nPlease help me to merge this two things together and make it a coherent new outline that show in Traditional Chinese. The new outline should follow the template:\noutline:\n" 
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p}
        ]
    )
    print("start print response:\n",chat.choices[0].message['content'])
    NewOutline=chat.choices[0].message['content'].split('outline:')
    
    return NewOutline

def GenerateDetails(api_key,organization,NameOfDB,WorkingChapter):
    openai.api_key = api_key
    openai.organization = organization
    content = fsql.TakeContent(NameOfDB, WorkingChapter)
    p = "Here is the original outline of the article :\n"+content+"\nPlease give me 3 places that added details can make the article more complete and intriguing. Those details should follow the template:\nD.\nD.\nD.\n Please show in Traditional Chinese only" 
    
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p}
        ]
    )
    print("start print response\n",chat.choices[0].message['content'])
    x=chat.choices[0].message['content'].split('\n')
    tmp=[]
    for i in range(len(x)) :
        tmp.append(x[i].split('. '))

    Details=[]
    for i in range(len(tmp)):
        if(len(tmp[i])>1):
             Details.append(tmp[i][1])

    return  Details