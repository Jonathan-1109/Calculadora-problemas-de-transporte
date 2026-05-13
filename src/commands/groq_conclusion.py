import groq


def groq_conclusion(client: groq.Groq, content: str, system_prompt: str = "") -> str | None:
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": content})

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            max_tokens=600,
            timeout=10.0,
        )
        return chat_completion.choices[0].message.content

    except groq.RateLimitError as e:
        print(f"[Groq] Límite de tokens alcanzado: {e}")
        return None
    except groq.APIConnectionError as e:
        print(f"[Groq] Error de conexión: {e}")
        return None
    except Exception as e:
        print(f"[Groq] Error inesperado: {e}")
        return None