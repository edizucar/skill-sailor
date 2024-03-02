from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
WHITELIST = "abcdefghijklmnopqrstuvwxyz"
MODEL="gpt-3.5-turbo"

def remove_non_whitelisted_chars(input_string, whitelist):
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
    system_message="You are a helpful individual that answers queries as accurately as possible."

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

if __name__ == "__main__":
    a = simpleCall("hello")
    b = getTextOfResponse(a)
    print(b)
