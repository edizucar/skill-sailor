from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()

WHITELIST = "abcdefghijklmnopqrstuvwxyz.,-:1234567890 "
MODEL="gpt-3.5-turbo"
SYS_PROMPT = "You are a careers advisor and summarise the path to starting a career as an immigrant in the UK based on the education, experience, and skills listed in their profile. The profile will be contained in triple angle braces."
BASE_PROMPT = 'Summarise in less than five bullet points the steps and requirements the person with the following profile should undertake to start the following career as a freash immigrant in the UK: {0}. Do not include any additional text. \nProfile:\n'

TEST_PROFILE = {'education': 'bachelor of science in computer science from new york university, graduated in may 2010. specialisations in full stack development with experience in leading teams, designing and implementing scalable architectures, developing restful apis, integrating third-party services, and working with various programming languages and databases.', 
                'experience': 'the candidate has the following work experience:1. senior full stack developer at openai in san francisco from july 2016 to present.   - led a team in designing and implementing a scalable microservices architecture.   - developed and maintained restful apis using node.js, express, and mongodb.   - designed and implemented front-end interfaces using react and angular.   - integrated third-party apis for payment processing and user authentication.   - implemented automated testing with jest and cypress.2. full stack developer at tesla in austin from january 2011 to june 2016.   - collaborated on delivering web applications.   - developed backend services and apis using python with django and flask.   - designed user interfaces using html, css, and javascript.   - conducted code reviews and provided feedback.', 
                'languages': 'spoken languages: english, japanese b1, german intermediate.', 
                'skills': '- programming languages: javascript, node.js, react, angular, python- databases: mongodb, mysql, postgresql- web technologies: html5, css3, restful apis, graphql- version control: git, github- development tools: vs code, docker, postman- testing: jest, cypress'
                }

TEST_PROFILE_2 = {'education': 'bachelor of arts in history from colombia city university in colombia. no further education history provided.', 
                  'experience': 'work experience:1. baker at estebanitas bakery family business - produced baked goods, managed inventory, developed recipes.2. event organizer - organized successful concerts, managed budgets, negotiated contracts, handled promotion.3. secretary at consulting office - provided administrative support, assisted in report preparation, maintained office files.', 
                  'languages': 'the spoken languages listed on the resume are spanish native and english proficient.', 
                  'skills': 'skills listed:1. proficient in microsoft office suite word, excel, powerpoint2. strong organizational and time management skills3. excellent communication and interpersonal abilities4. skilled amateur painter5. fluent in spanish6. proficient in english.'}


def getSummary(profile, specialisation):
    """
    Returns a list of three potential job specialisations for the user to join.

    Parameters:
        profile (dict): a dict populated with user information
        industry (str): the labour market sector chosen in stage 1
        job (str): the generic job the user has selected in the previous stage
    Returns:
        industries (dict): a dict containing the list of three job specialisations to be listed on the stage one tiles under key "payload"
    """

    prompt = BASE_PROMPT.format(specialisation) + "<<<" + profileToStr(profile) + ">>>"
    response = simpleCall(prompt, 1)        
    summary = getTextOfResponse(response, 0)
    return {"payload": summary}

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

def simpleCall(message, responseCount):
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
        ],
        n=responseCount
    )

    return response

def getTextOfResponse(response, choice):
    text = ""
    try:
        text=response.choices[choice].message.content
    except Exception:
        raise ValueError
    return text

def profileToStr(profile):
    result =  ", ".join([f"{key}: {value}" for key, value in profile.items()])
    return result

if __name__ == "__main__":
    print(getSummary(TEST_PROFILE_2, "Administrative Specialist: Your experience as a secretary providing administrative support and maintaining office files aligns well with the responsibilities of an Administrative Specialist, which includes managing office operations, coordinating meetings, and handling correspondence.")["payload"])