from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()

WHITELIST = "abcdefghijklmnopqrstuvwxyz.,-:1234567890 "
MODEL="gpt-3.5-turbo"
TEST_CV_FILE = "backend/test_cv.txt"

SYS_PROMPT = "You are a careers advisor and recommend the best job specialisations for people based on the education, experience, and skills listed in their profile, and their chosen job. The profile will be contained in triple angle braces."
BASE_PROMPT = 'Suggest the top three different specialisations of the job \"{1}\" in the {0} sector tailored for the person with the following education and experience. Recommend exclusively specialisations highly relevant to the job \"{1}\" in the sector: \"{0}\". Return only the job titles with a single sentence describing how this applicant\'s skills fit this job in the format of a python dictionary, for example: dictionary("Specialisation 1": "Description 1", "Specialisation 2": "Description 2", "Specialisation 3": "Description 3"). Do not include ```python```. \nProfile:\n'

TEST_PROFILE = {'education': 'bachelor of science in computer science from new york university, graduated in may 2010. specialisations in full stack development with experience in leading teams, designing and implementing scalable architectures, developing restful apis, integrating third-party services, and working with various programming languages and databases.', 
                'experience': 'the candidate has the following work experience:1. senior full stack developer at openai in san francisco from july 2016 to present.   - led a team in designing and implementing a scalable microservices architecture.   - developed and maintained restful apis using node.js, express, and mongodb.   - designed and implemented front-end interfaces using react and angular.   - integrated third-party apis for payment processing and user authentication.   - implemented automated testing with jest and cypress.2. full stack developer at tesla in austin from january 2011 to june 2016.   - collaborated on delivering web applications.   - developed backend services and apis using python with django and flask.   - designed user interfaces using html, css, and javascript.   - conducted code reviews and provided feedback.', 
                'languages': 'spoken languages: english, japanese b1, german intermediate.', 
                'skills': '- programming languages: javascript, node.js, react, angular, python- databases: mongodb, mysql, postgresql- web technologies: html5, css3, restful apis, graphql- version control: git, github- development tools: vs code, docker, postman- testing: jest, cypress'
                }

TEST_PROFILE_2 = {'education': 'bachelor of arts in history from colombia city university in colombia. no further education history provided.', 
                  'experience': 'work experience:1. baker at estebanitas bakery family business - produced baked goods, managed inventory, developed recipes.2. event organizer - organized successful concerts, managed budgets, negotiated contracts, handled promotion.3. secretary at consulting office - provided administrative support, assisted in report preparation, maintained office files.', 
                  'languages': 'the spoken languages listed on the resume are spanish native and english proficient.', 
                  'skills': 'skills listed:1. proficient in microsoft office suite word, excel, powerpoint2. strong organizational and time management skills3. excellent communication and interpersonal abilities4. skilled amateur painter5. fluent in spanish6. proficient in english.'}

def getSpecialisations(profile, industry, job):
    """
    Returns a list of three potential job specialisations for the user to join.

    Parameters:
        profile (dict): a dict populated with user information
        industry (str): the labour market sector chosen in stage 1
        job (str): the generic job the user has selected in the previous stage
    Returns:
        industries (dict): a dict containing the list of three job specialisations to be listed on the stage one tiles under key "payload"
    """

    prompt = BASE_PROMPT.format(industry, job) + "<<<" + profileToStr(profile) + ">>>"
    response = simpleCall(prompt, 3)
    for attempt in range(3):
        specialisations = getTextOfResponse(response, attempt)
        try:
            specialisationsDict = json.loads(specialisations)
            break
        except Exception:
            print("Could not load specialisations dictionary in attempt: " + str(attempt))
        raise Exception("Could not load response dict.")

    a = []
    for key in specialisationsDict.keys():
        a.append(key + ": " + specialisationsDict[key])
    return {"payload": a}

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
    print(getSpecialisations(TEST_PROFILE_2, "Administrative", "Office Manager")["payload"])