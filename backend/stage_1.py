from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

WHITELIST = "abcdefghijklmnopqrstuvwxyz.,-:1234567890 "
MODEL="gpt-3.5-turbo"
TEST_CV_FILE = "backend/test_cv.txt"

SYS_PROMPT = "You are a careers advisor and recommend the best labour market sectors in the UK for immigrants based on the education, experience, and skills in their profile. You do not add any comments. The profile will be contained in triple angle braces."
BASE_PROMPT = "Suggest three different, diverse labour market sectors where the person with the following profile could find a job. Be creative. Return only the names of the sectors without further comments in the format of a python list, for example: ['Sector 1', 'Sector 2', 'Sector 3'].\n"

TEST_PROFILE = {'education': 'bachelor of science in computer science from new york university, graduated in may 2010. specialisations in full stack development with experience in leading teams, designing and implementing scalable architectures, developing restful apis, integrating third-party services, and working with various programming languages and databases.', 
                'experience': 'the candidate has the following work experience:1. senior full stack developer at openai in san francisco from july 2016 to present.   - led a team in designing and implementing a scalable microservices architecture.   - developed and maintained restful apis using node.js, express, and mongodb.   - designed and implemented front-end interfaces using react and angular.   - integrated third-party apis for payment processing and user authentication.   - implemented automated testing with jest and cypress.2. full stack developer at tesla in austin from january 2011 to june 2016.   - collaborated on delivering web applications.   - developed backend services and apis using python with django and flask.   - designed user interfaces using html, css, and javascript.   - conducted code reviews and provided feedback.', 
                'languages': 'spoken languages: english, japanese b1, german intermediate.', 
                'skills': '- programming languages: javascript, node.js, react, angular, python- databases: mongodb, mysql, postgresql- web technologies: html5, css3, restful apis, graphql- version control: git, github- development tools: vs code, docker, postman- testing: jest, cypress'
                }

TEST_PROFILE_2 = {'education': 'bachelor of arts in history from colombia city university in colombia. no further education history provided.', 
                  'experience': 'work experience:1. baker at estebanitas bakery family business - produced baked goods, managed inventory, developed recipes.2. event organizer - organized successful concerts, managed budgets, negotiated contracts, handled promotion.3. secretary at consulting office - provided administrative support, assisted in report preparation, maintained office files.', 
                  'languages': 'the spoken languages listed on the resume are spanish native and english proficient.', 
                  'skills': 'skills listed:1. proficient in microsoft office suite word, excel, powerpoint2. strong organizational and time management skills3. excellent communication and interpersonal abilities4. skilled amateur painter5. fluent in spanish6. proficient in english.'}

def getIndustries(profile):
    """
    Returns a list of three potential industries for the user to join.

    Parameters:
        profile (dict): a dict populated with user information 
    Returns:
        industries (dict): a dict containing the list of three industries to be listed on the stage one tiles under key "payload"
    """
    prompt = BASE_PROMPT + "<<<" + profileToStr(profile) + ">>>"
    response = simpleCall(prompt)
    industries = getTextOfResponse(response, 0)
    # for choice in range(3):
    #     industries.append()
    return {"payload": industries}

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
        ],
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
    print(getIndustries(TEST_PROFILE_2)["payload"])
