from openai import OpenAI

print("test running...")
client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a careers advisor, with knowledge of the UK job market. You give each user three most suitable career paths."},
        {"role": "user", "content": "Suggest a career path for a mathematics masters graduate with experience in python for statistics."}
    ]
)

print(completion.choices[0].message)