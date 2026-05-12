import groq

def groq_conclusion(client: groq.Groq, content: str):

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user","content": content,}],
            model="llama-3.3-70b-versatile",
        )
        print(chat_completion.choices[0].message.content)
    except groq.RateLimitError as e:
        print("Limite de tokens alcanzado: " + str(e))
    except Exception as e:
        print(e)