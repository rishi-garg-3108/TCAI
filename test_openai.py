from openai import OpenAI

client = OpenAI(api_key="your api key")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":"Return JSON: {\"category\":\"test\",\"confidence\":0.9,\"reasoning\":\"test\"}"}]

)

print(response.choices[0].message.content)