from groq import Groq

def groqClient(apikey, content):
    client = Groq(
        api_key=apikey,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)