from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

WHITELIST = "abcdefghijklmnopqrstuvwxyz.,-:1234567890 "
SYS_PROMPT = "You extract and realistically summarise information from CVs and output them in 1-2 sentences. You do not add any comments. The CV will be contained in triple angle braces."
MODEL="gpt-3.5-turbo"
TEST_CV_FILE = "backend/test_cv_2.txt"

promptsDict = {
    "education":"Extract and summarise in 1-2 sentences the highest achieved degree of education and specialisation from the following resume. If any piece of information can't be obtained, output \"No education history\".",
    "experience":"Extract the work experience from the following resume. If any piece of information can't be obtained, output \"No work history\".",
    "languages":"Extract the spoken languages from the following resume. If any piece of information can't be obtained, output \"No listed languages\".",
    "skills":"Extract the listed skills from the following resume. If any piece of information can't be obtained, output \"No listed skills\"."
    }

def cvToProfile(cv):
    """
    Extract education, experience, spoken languages and skills from a CV and populate a profile dictionary with them.

    Parameters:
        cv (str): the name of a cv file in txt format

    Returns:
        profile (dict): A JSON dictionary containing the Education, Experience, and Skill lists.
    """
    cvClean = removeNonWhitelistedChars(cv, WHITELIST)
    profile = {}
    for category in promptsDict.keys():
        prompt = promptsDict[category] + "\n" + "<<<" + cvClean + ">>>"
        response = simpleCall(prompt)
        output = getTextOfResponse(response)
        outputClean = removeNonWhitelistedChars(output, WHITELIST)
        profile[category] = outputClean

    return profile

def readCv(fileName):
    with open(fileName) as f:
        cv = f.read()
    return cv

def readPrompt(fileName):
    with open(fileName) as f:
        prompt = f.readlines()
    return prompt

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
    system_message=SYS_PROMPT

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
