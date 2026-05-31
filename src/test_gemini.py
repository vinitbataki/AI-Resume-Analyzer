from google import genai
client = genai.Client(api_key="AQ.Ab8RN6IaA2Us6T4JR-cqzzclEyqojv9h2oNUERXHFwDB0K-AsA")

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="say hello"
)

print(response.text)