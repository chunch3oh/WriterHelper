import logging
import os
from typing import List

import openai
from dotenv import load_dotenv
from langchain import ConversationChain, LLMChain, OpenAI, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from pydantic import BaseModel, Field, validator

import FunctionOfSQLite as fsql


def init_env():
    # Load environment variables
    load_dotenv()
    openai_org = os.getenv("OPENAI_ORG")
    if openai_org is not None:
        openai.organization = openai_org
        logging.warning(f"Switching to organization: {openai_org} for OAI API key.")
    openai.api_key = os.getenv("OPENAI_API_KEY")


def user_input_content():
    # Define a list of prompts.

    prompts = [
        "故事類型（例如：魔幻、科幻、愛情、歷險、神秘、驚悚、恐怖等）：",
        "主要角色（例如：角色的名字、年齡、職業、性格、專長等）：",
        "輔助角色（例如：角色的名字、年齡、職業、性格、專長等）：",
        "時間（例如：過去、現在、未來、特殊時代、特殊年代等）：",
        "地點（例如：城市、村莊、森林、海底、外星球、夢境等）：",
        "起始情境（例如：角色在做什麼、突發何種事件、遇到了什麼困難等）：",
        "主要衝突（例如：角色與他人的矛盾、與環境的衝突、與自己內心的鬥爭等）：",
        "高潮（例如：衝突或困難的高度點、角色的決定性行動等）：",
        "結局（例如：衝突或困難的解決方式、角色的終點、新的開始等）：",
    ]

    # Define columns for the database table.
    columns = [
        "type",
        "main_character",
        "supporting_characters",
        "time_period",
        "setting",
        "initial_situation",
        "conflict",
        "climax",
        "resolution",
    ]

    # Use list comprehension to get user input for each prompt.
    # values = [input(prompt) for prompt in prompts]

    values = [
        "冒險故事",
        "艾莉絲",
        "貝克、蘿拉",
        "現代",
        "一座神秘島嶼",
        "艾莉絲是一名探險家，她聽說傳說中有一座神秘島嶼，據說蘊藏著無數寶藏和神奇的力量。她決定前往尋找這座島嶼，但沒有人知道島嶼的確切位置。",
        "艾莉絲必須克服無數的困難和危險，包括陡峭的山崖、叢林中的危險生物，以及隱藏的陷阱和謎題，才能找到這座神秘島嶼。",
        "在艾莉絲即將放棄的時候，她遇到了一位當地居民貝克，他提供了一些關鍵的線索和幫助，讓艾莉絲重新振作起來。",
        "最終，艾莉絲成功找到了神秘島嶼，發現了它的寶藏和神奇力量。她和貝克、蘿拉一起分享了這個驚奇的發現，並帶回了一些寶藏作為紀念。艾莉絲的冒險不僅帶給她財富，更讓她學到了勇氣和堅持的重要性，並結交了一生的好朋友。",
    ]

    # Create table and insert values.
    fsql.create_table("Story", columns)
    fsql.insert_values("Story", columns, values)


class StoryOutline(BaseModel):
    chapter_1_name: str = Field(description="chapter name")

    chapter_2_name: str = Field(description="chapter name")

    chapter_3_name: str = Field(description="chapter name")

    chapter_4_name: str = Field(description="chapter name")

    chapter_5_name: str = Field(description="ending chapter name")


def start_adding_outline():
    attribute_names = [
        "type",
        "main_character",
        "supporting_characters",
        "time_period",
        "setting",
        "initial_situation",
        "conflict",
        "climax",
        "resolution",
    ]
    attributes = {name: fsql.get_content("Story", name) for name in attribute_names}

    template = """
    故事類型：{type}
    主要角色：{main_character}
    輔助角色：{supporting_characters}
    時間：{time_period}
    地點：{setting}
    起始情境：{initial_situation}
    主要衝突：{conflict}
    高潮：{climax}
    結局：{resolution}

    請根據上述内容生成章節名稱。
    {format_instructions}
    """
    parser = PydanticOutputParser(pydantic_object=StoryOutline)
    prompt = PromptTemplate(
        template=template,
        input_variables=list(attributes.keys()),
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    outline = prompt.format_prompt(**attributes)

    model = OpenAI(temperature=0.8)
    model_output = model(outline.to_string())

    parser = PydanticOutputParser(pydantic_object=StoryOutline)
    story_outline = parser.parse(model_output)

    story_data = story_outline.dict()

    for column, content in story_data.items():
        fsql.add_column("Story", column, content)


# TODO: 生成的大綱長度有限，還沒生完就結束了。
def generate_and_store_outline_to_db():
    # Get the chapter names from the database
    chapter_names = [
        fsql.get_content("Story", "chapter_" + str(i) + "_name") for i in range(1, 6)
    ]

    # Initialize the AI model
    model = OpenAI(temperature=0.8)

    attribute_names = [
        "type",
        "main_character",
        "supporting_characters",
        "time_period",
        "setting",
        "initial_situation",
        "conflict",
        "climax",
        "resolution",
    ]
    attributes = {name: fsql.get_content("Story", name) for name in attribute_names}

    outline = ""
    for i, chapter_name in enumerate(chapter_names):
        template = ""
        if i == 0:
            template = """
            故事類型：{type}
            主要角色：{main_character}
            輔助角色：{supporting_characters}
            時間：{time_period}
            地點：{setting}
            起始情境：{initial_situation}
            主要衝突：{conflict}
            高潮：{climax}
            結局：{resolution}

            第{order}章：{chapter_name}:
            """
        else:
            template = """
            {Previous_chapter_outline}
    
            第{order}章：{chapter_name}:
            """

        prompt = template.format(
            Previous_chapter_outline=outline,
            order=str(i + 1),
            chapter_name=chapter_name,
            **attributes,
        )

        # Generate the outline for this chapter
        chapter_outline = model(prompt)

        # Update the outline
        outline += f"\n第{i + 1}章: {chapter_name}\n{chapter_outline}"

        print(outline)

        # Store the outline in the database
        fsql.add_column("Story", f"chapter_{i + 1}_outline", chapter_outline)


def continue_questions_answers_and_outlining():
    # 提取章節名稱以及對應的大綱

    # 根據大綱生成問題

    # 使用者可以回答問題，或是跳過問題

    # 根據回答的問題，更新大綱

    # 重複上述步驟，直到使用者滿意為止

    # 將大綱儲存到資料庫 [更新]
    pass


def update_outline_in_db():
    pass


def output_final_outline_when_satisfied():
    pass


def workflow():
    # 讓使用者填充內容
    user_input_content()

    # 開始補充大綱（根據人、事、時、地、物）
    start_adding_outline()

    # 根據上述内容生成大綱，並儲存到資料庫
    generate_and_store_outline_to_db()

    # 持續生成問題以及回答問題，補充大綱，直到滿意為止
    continue_questions_answers_and_outlining()

    # 將大綱儲存到資料庫 [更新]
    update_outline_in_db()

    # 直到使用者滿意為止，就可以輸出大綱了
    output_final_outline_when_satisfied()


if __name__ == "__main__":
    init_env()

    workflow()
