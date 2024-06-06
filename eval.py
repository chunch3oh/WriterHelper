import os
import openai


def create_criteria_dictionary(directory):
    file_dict = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and filename.startswith("eval"):
            key = filename.replace("eval-", "").replace(".txt", "")
            with open(os.path.join(directory, filename), "r") as file:
                value = file.read()
                file_dict[key] = value
    return file_dict


def create_story_dictionary(directory):
    file_dict = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            key = filename
            with open(os.path.join(directory, filename), "r") as file:
                value = file.read()
                file_dict[key] = value
    return file_dict


def score_story(story_name, story_content, criteria):
    result_file_path = os.path.join(result_directory_path, story_name)
    if os.path.exists(result_file_path):
        print(f"Skipping the story {story_name} as it has already been evaluated.")
        return

    print(f"For story: {story_name}")
    print(story_content)
    with open(result_file_path, "w") as result_file:
        for metric_name, prompt_template in criteria.items():
            replace_string = f"{story_content}"
            prompt = prompt_template.replace("{{Story}}", replace_string)

            chat = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )

            response = chat.choices[0].message["content"]
            result_file.write(f"For metric {metric_name}:\n{response}\n\n")

            print(f"For metric {metric_name}")
            print(response)


openai.api_key = "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"
openai.organization = "org-fHMALWhrQo5GJy97j84kLWbv"

directory_path = "./PromptTemplate"
criteria = create_criteria_dictionary(directory_path)

story_directory_path = "./Gallery"
story_dict = create_story_dictionary(story_directory_path)

result_directory_path = "./Result"

if not os.path.exists(result_directory_path):
    os.makedirs(result_directory_path)

for story_name, story in story_dict.items():
    score_story(story_name, story, criteria)


