import google.generativeai as genai # Import the generative AI module

genai.configure(api_key='AIzaSyCyo1cZCpSXwsrk6HqUGKHIDBU3BZuNc1U')
model=genai.GenerativeModel('gemini-pro')
response=model.generate_content("I am feeling sad today because")
print(response.text)