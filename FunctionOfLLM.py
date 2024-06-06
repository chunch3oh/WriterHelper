import openai
import random
import csv
import os
import re
import FunctionOfSQLite as fsql
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
import json
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser


def generate_story_title_list(style, time, place, other_info):
    # Create a template for the variables
    template = """
    Please use Traditional Chinese to generate a random story outline based on the following information:
    Style: {style}
    Time: {time}
    Place: {place}
    Other_information: {other_information}

    The story outline should consist of four chapters, each with its specific role in the narrative:
    1. Exposition (起): This chapter introduces the background, characters, and initial events.
    2. Development (承): This chapter contains the progression and development of the plot.
    3. Climax (转): This chapter includes the turning point or climax of the story.
    4. Resolution (合): This chapter concludes and resolves conflicts.
    
    story_outline_1: The title of the first chapter. (Exposition)
    story_outline_2: The title of the second chapter. (Development)
    story_outline_3: The title of the third chapter. (Climax)
    story_outline_4: The title of the fourth chapter. (Resolution)

    Format the output as JSON with the following keys:
    story_outline_1
    story_outline_2
    story_outline_3
    story_outline_4
    """

    prompt_template = ChatPromptTemplate.from_template(template=template)

    story_outline_1_schema = ResponseSchema(
        name="story_outline_1",
        description="The title of the first chapter. (Exposition)",
    )

    story_outline_2_schema = ResponseSchema(
        name="story_outline_2",
        description="The title of the second chapter. (Development)",
    )

    story_outline_3_schema = ResponseSchema(
        name="story_outline_3",
        description="The title of the third chapter. (Climax)",
    )

    story_outline_4_schema = ResponseSchema(
        name="story_outline_4",
        description="The title of the fourth chapter. (Resolution)",
    )

    response_schemas = [
        story_outline_1_schema,
        story_outline_2_schema,
        story_outline_3_schema,
        story_outline_4_schema,
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    messages = prompt_template.format_messages(
        style=style,
        time=time,
        place=place,
        other_information=other_info,
        format_instructions=format_instructions,
    )

    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=1.0)

    response = chat(messages)
    story_outline_dict = output_parser.parse(response.content)

    chapter_name_list = list(story_outline_dict.values())

    return chapter_name_list


def generate_story_outline(story_title_list, style, time, place, other_info):
    template = """
    Style: {style}
    Time: {time}
    Place: {place}
    Other_information: {other_information}

    List of Story Titles:
    {story_title_list}

    Previously Developed Content:
    {previous_content}

    Upcoming Chapter: {story_title}

    Your task: Please create a four-sentence story outline in a traditional Chinese context continuing from the previously developed content. The outline should directly relate to the upcoming chapter. 

    Please provide the story outline as plain text.
    """

    prompt_template = ChatPromptTemplate.from_template(template=template)
    all_outlines = []

    for story_title in story_title_list:
        messages = prompt_template.format_messages(
            style=style,
            time=time,
            place=place,
            other_information=other_info,
            story_title_list="\n".join(story_title_list),
            previous_content="\n".join(all_outlines),
            story_title=story_title,
        )

        chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
        response = chat(messages)

        all_outlines.append(response.content)

    return all_outlines


def GenerateOutline(
    Style="random", Time="random", Place="random", OtherInformation="random"
):
    """
    Generate a story outline and return a list of outline.
    """

    # Create a list of variables for the template of story outline
    styles = [
        "奇幻",
        "偵探推理",
        "寫實主義",
        "愛情",
        "歷史劇",
        "靈異驚悚",
        "武俠傳奇",
        "蒸汽朋克",
        "科幻冒險",
        "懸疑驚悚",
        "古典神話",
        "宇宙探險",
    ]
    times = [
        "戰國時代",
        "唐朝",
        "中世紀",
        "清朝",
        "未來世紀",
        "太空時代",
        "二戰期間",
        "石器時代",
        "前現代",
        "近未來",
        "遙遠未來",
        "西元前",
    ]
    places = [
        "魔法學院",
        "大海探險",
        "荒蕪星球",
        "古老神殿",
        "宮廷深宅",
        "龍的洞穴",
        "異次元世界",
        "地底城市",
        "月球基地",
        "虛擬現實",
        "神秘森林",
        "蒸汽朋克城市",
    ]
    other_infos = [
        "十二生肖的傳說",
        "時間旅行的哲學",
        "異種戀人的羈絆",
        "人與AI的關係",
        "精神分裂的困擾",
        "超能力的秘密",
        "人類克隆的道德問題",
        "疫情下的生存掙扎",
    ]

    style = Style if Style != "random" else random.choice(styles)
    time = Time if Time != "random" else random.choice(times)
    place = Place if Place != "random" else random.choice(places)
    other_info = (
        OtherInformation if OtherInformation != "random" else random.choice(other_infos)
    )

    # Generate a list of chapter names
    chapter_name_list = generate_story_title_list(style, time, place, other_info)

    # Generate a list of story outlines
    story_outlines = generate_story_outline(
        chapter_name_list, style, time, place, other_info
    )

    return story_outlines


def Expand(api_key, organization, Reply, QD):
    openai.api_key = api_key
    openai.organization = organization
    p = (
        "Here's a sentence:\n"
        + Reply
        + "\nPlease make it more coherent according to the following questions or details:\n"
        + QD
        + "\nYou should reply in Traditional Chinese and follow this template :\n R:\n"
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p},
        ],
    )

    print(chat.choices[0].message["content"])

    x = chat.choices[0].message["content"].split("R:")

    return x[1]


def GenerateKeyWords(api_key, organization, outline):
    openai.api_key = api_key
    openai.organization = organization
    p = (
        "please generate few key words includes: 人、事、時、地、物 and based on the following article. If there's nothing is matched then just print 無, also, if there's more than 2 items then use ',' to seperate them. Your output should follow this template\n人:\n事:\n時:\n地:\n物:\n, please show the result in Traditional Chinese :\n"
        + outline
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p},
        ],
    )

    print(chat.choices[0].message["content"])

    x = chat.choices[0].message["content"].split("\n")
    tmp = []

    for i in range(len(x)):
        tmp.append(re.split(": |：", x[i]))

    KeyWords = []
    KeyWords.append(tmp[0][1].split(","))
    KeyWords.append(tmp[1][1].split(","))
    KeyWords.append(tmp[2][1].split(","))
    KeyWords.append(tmp[3][1].split(","))
    KeyWords.append(tmp[4][1].split(","))

    return KeyWords


def GenerateQuestions(api_key, organization, KeyWordsChosen, NameOfDB, WorkingChapter):
    openai.api_key = api_key
    openai.organization = organization
    content = fsql.TakeContent(NameOfDB, WorkingChapter)
    p = (
        "Here is the original outline of the article :\n"
        + content
        + "\nPlease give me 3 questions related to "
        + KeyWordsChosen
        + "that added can make the article more complete and intriguing. Those questions should follow the template:\nQ.\nQ.\nQ.\n Please show in Traditional Chinese only"
    )

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p},
        ],
    )
    print("start print response\n", chat.choices[0].message["content"])
    x = chat.choices[0].message["content"].split("\n")
    tmp = []
    for i in range(len(x)):
        tmp.append(x[i].split(". "))

    Questions = []
    for i in range(len(tmp)):
        if len(tmp[i]) > 1:
            Questions.append(tmp[i][1])

    return Questions


def MergeOutlineByQuestions(api_key, organization, Reply, NameOfDB, WorkingChapter):
    openai.api_key = api_key
    openai.organization = organization
    content = fsql.TakeContent(NameOfDB, WorkingChapter)
    p = (
        "Here is the original outline of the article :\n"
        + content
        + "\nAlso, here is some reply that we think that can make the outline better\n"
        + Reply
        + "\nPlease help me to merge this two things together and make it a coherent new outline that show in Traditional Chinese. The new outline should follow the template:\noutline:\n"
    )

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p},
        ],
    )
    print("start print response:\n", chat.choices[0].message["content"])
    NewOutline = chat.choices[0].message["content"].split("outline:")

    return NewOutline


def GenerateDetails(api_key, organization, NameOfDB, WorkingChapter):
    openai.api_key = api_key
    openai.organization = organization
    content = fsql.TakeContent(NameOfDB, WorkingChapter)
    p = (
        "Here is the original outline of the article :\n"
        + content
        + "\nPlease give me 3 places that added details can make the article more complete and intriguing. Those details should follow the template:\nD.\nD.\nD.\n Please show in Traditional Chinese only"
    )

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Executive Editor."},
            {"role": "user", "content": p},
        ],
    )
    print("start print response\n", chat.choices[0].message["content"])
    x = chat.choices[0].message["content"].split("\n")
    tmp = []
    for i in range(len(x)):
        tmp.append(x[i].split(". "))

    Details = []
    for i in range(len(tmp)):
        if len(tmp[i]) > 1:
            Details.append(tmp[i][1])

    return Details
