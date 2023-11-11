from PyPDF2 import PdfReader
import os, openai
from youtube_transcript_api import YouTubeTranscriptApi

openai.api_key = "YOUR_API_KEY_HERE"
if openai.api_key == "YOUR_API_KEY_HERE":
    print("Please replace the value of the variable openai.api_key with your OpenAI API key in skimpdf.py before running the program. Aborting.")
    exit()

print("*" * 50)
print("skimbot v1")
print("*" * 50)
print("Developed by Azhaan Salam under the MIT License, which allows you to use this code for any purpose, commercial or non-commercial\n")
print("Distributing this software without the original license may be a violation of the license agreement and could be subject to legal action.")
print("*" * 50)
print("This program uses the OpenAI API to generate a summary of a PDF file / YouTube video. Please note that the OpenAI API is a paid service and you will be charged for using it.")
print("You can find out more about the OpenAI API at https://openai.com/blog/openai-api/")
print("*" * 50)
print("Choose a mode:")
print("[1]: PDF")
print("[2]: YouTube video")
print()
mode = int(input("Enter the number of the mode you want to use: "))
print("*" * 50)
if mode == 1:
    pdfs = []
    for file in os.listdir():
        if file.endswith(".pdf"):
            pdfs.append(file)
    print("Found " + str(len(pdfs)) + " PDF(s) in the current directory.\n")
    if len(pdfs) == 0:
        print("No PDFs found. Please add a PDF file to the directory to skim through. Aborting.")
        exit()
    print("Choose a PDF to skim:")
    for i in range(len(pdfs)):
        print(f"[{i}]: {pdfs[i]}")
    print()
    selection = int(input("Enter the number of the PDF you want to skim: "))
    if selection < 0 or selection >= len(pdfs):
        print("Invalid selection. Aborting.")
        exit()
    print("*" * 50)
    selection = pdfs[selection]
    print("✅ Getting ready to skim " + selection + "...")
    print("*" * 50)
    reader = PdfReader(selection)
    number_of_pages = len(reader.pages)
    full_text = ""
    for i in range(number_of_pages):
        full_text += " ".join(reader.pages[i].extract_text().split("\n"))
        full_text += "\n"
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Provide a detailed summary on the following text:\n" + full_text}]
    )
    print("Done. Outputting summary...")
    print("*" * 50)
    print(summary['choices'][0]['message']['content'])
elif mode == 2:
    id = input("Enter the video ID of the YouTube video you want to skim (enter h for help): ")
    while id == "h":
        print("\nThe video ID is the part of the YouTube video URL after the v= part.")
        print("For example, if the URL of the video is https://www.youtube.com/watch?v=abc123, the video ID is abc123.\n")
        id = input("Enter the video ID of the YouTube video you want to skim (enter h for help): ")
    print("*" * 50)
    print("✅ Getting ready to skim YouTube video " + "with url https://www.youtube.com/watch?v="+ id + "...")
    print("*" * 50)
    transcript = YouTubeTranscriptApi.get_transcript(id)
    list_of_text = []
    for i in transcript:
        list_of_text.append(i['text'])
    full_text = " ".join(list_of_text)
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Provide a detailed summary on the following video transcript:\n" + full_text}]
    )
    print("Done. Outputting summary...")
    print("*" * 50)
    print(summary['choices'][0]['message']['content'])
else:
    print("Invalid mode. Aborting.")
    exit()