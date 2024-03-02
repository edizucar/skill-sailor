from openai import OpenAI
import os
import json

from dotenv import load_dotenv
load_dotenv()

WHITELIST = "abcdefghijklmnopqrstuvwxyz"
PROMPT_FILE = "backend/prompt_cv_to_profile.txt"
SYS_PROMPT_FILE = "backend/sys_prompt_cv_to_profile.txt"
MODEL="gpt-3.5-turbo"
TEST_CV_FILE = "backend/test_cv.txt"

def cvToProfile(cvFile):
    """
    Extract education, experience, spoken languages and skills from a CV and populate a profile dictionary with them.

    Parameters:
        cv (str): the name of a cv file in txt format

    Returns:
        profile (dict): A JSON dictionary containing the Education, Experience, and Skill lists.
    """
    with  open(PROMPT_FILE) as f:
        prompt = f.read()
    with open(cvFile) as f:
        cv = f.read()
    prompt += "\n" + cv
    messageClean = removeNonWhitelistedChars(prompt, WHITELIST)
    try:
        response = simpleCall(messageClean)
        output = getTextOfResponse(response)
        print(output)
        profile = json.loads(output)
    except Exception:
        raise ValueError("GPT Output profile not a valid JSON: \n" + output)

    return profile

def removeNonWhitelistedChars(input_string, whitelist):
    """
    Remove characters from input_string that are not present in the whitelist.
    
    Parameters:
        input_string (str): The input string from which characters will be removed.
        whitelist (str): A string containing allowed characters.
        
    Returns:
        str: The input string with non-whitelisted characters removed.
    """
    return ''.join(char for char in input_string.lower() if char in whitelist)

def simpleCall(message):
    """
    Assume message is clean (no funky characters)
    """
    client = OpenAI()
    system_message=SYS_PROMPT_FILE

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content": system_message},
            {"role":"user","content": message}
        ]
    )

    return response

def getTextOfResponse(response):
    text = ""
    try:
        text=response.choices[0].message.content
    except Exception:
        raise ValueError
    return text

print(cvToProfile(TEST_CV_FILE))