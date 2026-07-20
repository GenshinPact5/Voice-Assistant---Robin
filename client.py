from openai import OpenAI

client = OpenAI(
    api_key="AQ.Ab8RN6LeWdwjljAqBR-9sh9fyoCur4ojduCl1Kke_I0QXKOprg",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

completion = client.chat.completions.create(
    model="gemini-2.5-pro",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named robin skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user", "content": "what is coding"}
    ]
)

print(completion.choices[0].message.content)





