# -*- coding: utf-8 -*-
"""Whispers of the Heart - Google AI Hackathon.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UAYRDz6eMsT8pQ5iMlaudnq1GyKxavVc

# Whispers of the Heart - A daily reflection journal

Journaling allows individuals to reflect on their thoughts, feelings, and experiences, promoting self-awareness and personal growth. As journals creates a safe space for a person to freely express their thoughts and feelings, therapists often use journals as a therapeutic tool to gain deeper insights into their clients' thoughts, feelings, and experiences.

## Library Imports
"""

#Importing the necessary libraries

import google.generativeai as genai

import pandas as pd
from datetime import date
import os

import PIL
from IPython.display import display, Markdown

# The API key import for the Gemini model
# Please use the submitted API key for running the model.
#
# If you are running this on Google Colab, use the Secrets panel
# (the key icon on the left panel) and add the API key, with the
# name GOOGLE_API_KEY and the key as the value. Switch on the
# Notebook Access button.

# Insert the API key here
GOOGLE_API_KEY=input("Please enter the Gemini API key: ")
genai.configure(api_key=GOOGLE_API_KEY)

"""## Initialising the variables"""

# Initialising the names of the files

data_folder = "data"
journal_file = "journal.txt"
analysis_file = "analysis.txt"

if "data" not in os.listdir():
  os.mkdir("data")

# Helper function to return the day of the week given the date

def day_of_the_week(date):
  weekday = date.weekday()
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  return days[weekday]

# Initialising today's date

today = date.today()
date_display = str(day_of_the_week(today)) + " - " + str(today.strftime("%B %d, %Y"))

# Helper function to write the entries to files

def writing_entry_to_file(entry, file_name):
  with open(os.path.join(data_folder, file_name), "a") as f:
    f.write(entry)

# Defining the prompt for the journal analysis

journal_prompt_template = '''

You are part of a journalling app, where the person will write about his everyday experience and share his thoughts and feelings.
But you are more than any ordinary journal. You will track the emotions and thoughts of the person and make observations out of it.

Finally you will summarise the person's mental state for the day.

The response should not make any conclusive decision about what the person should do, as that is the therapist's job.
The response should be an observation of the person's mental well-being and making an analysis of it, to help the therapist come up with the decisions.

You can use the previous day's journal entry to have a progression in emotions, but the analysis and the summary has to be only of today's journal entry.

The structure of the response should be:

**Emotions**: <A list of atleast 3 emotions they are going through.>
**Possible thought patterns**: <A collection of 3-4 prominent thought patterns the person is having with a brief explanation.>

**Mental well-being scores:**
<A list of 10-15 mental states of the person, with two scores - confidence (how sure you are about the state of the person) and intensity (the strength of the emotion in the person).
Make both the scores out of 10. Include all major mental health states.
Make it look like a table.
Sort the states in the decreasing order of the confidence scores>

**Summary of the day:** <The summary should be informative to the therapist. Highlight the progresson of the person's mental state from the previous days to the current day. Keep the summary in 3-4 sentences/>

**Journal Excerpts:** <Top 3 excerpts of the journal that helped you make these analysis. Take only a small snippet (or a few short phrases) of the journal entry for each excerpt. Break down your reasoning step-by-step. Give clarifications or explanations for the analysis. DO NOT display the personal identification information of the person or anyone that they speak about. Keep the privacy intact. You can replace their information with placeholders.>

Previous days' journal entry:
{journal_yesterday}
Today's journal entry:
{journal_today}
'''

# Defining hte prompt for the analysis of drawing

drawing_prompt_template = '''
You are a part of a journalling app, where the person will draw an image to convey his thoughts, feelings and mood.
But you are more than any ordinary journal. You will analyse and understand the emotions and thoughts of the person through the image.

You will also score the person's mental well-being on a few mental health 'symptoms' on a scale of 1 to 10 on how likely the person is in this state.
Finally you will summarise the person's mental state for the day.

The response should NOT make any conclusive decision about what the person should do, as that is the therapist's job.
The response should be an observation of the person's mental well-being and making an analysis of it, to help the therapist come up with the decisions.
The response should analyse the image and what the image is conveying and how the image is reflection of the person.

The structure of the response should be:

1. **Emotions**: <A list of atleast 3 emotions the image depicts.>
2. **Possible thought patterns**: <A collection of 3-4 prominent thought patterns the image is having with a brief explanation.>
3. **Mental well-being scores:**
<A list of 10-15 mental states as indicated by the image, with two scores - confidence (how sure you are about the state in the image) and intensity (the strength of the emotion in the image).
Make both the scores out of 10. Include all major mental health states.
Make it look like a table.
Sort the states in the decreasing order of the confidence scores>
4. **Summary of the day:** <The summary should be informative to the therapist. Keep the summary in 3-4 sentences/>
5. **Explanation:** <Explain your reasoning with detailed descriptions of the image. Break down your reasoning step-by-step. >
'''

user_type = input('Do you want to journal today? (J) Or are you a therapist? (T)? ')

if user_type == 'J' or user_type == 'j':

  """## Journal View

  This is what the journalling person views in the app.
  """

  # We are taking the inputs for the journal here.
  # The person can use the input text boxes to enter his thoughts from the day

  print("Daily Reflection Journal\n")

  # Printing out today's date

  print(date_display)

  # We have given a few thought-provoking questions to let the person reflect on his day.
  # The question can be skipped by just pressing the Enter key without writing anything.
  # Make sure to answer at least one question.
  # (We decided not to add the force input here. But if we develop an app over this we can
  # make sure to include this feature).

  experience = input("\nWhat emotions did I experience today and why?\n")
  lessons = input("\nDid I learn any insights or lessons from the day?\n")
  obstacles = input("\nWhat challenges or obstacles did I face today, and how did I approach them?\n")
  reflections = input("\nWhat are the key reflections from the day?\n")
  extra = input("\nDo you want to share anything else? Write a poem? Have a quote you relate to? Or just want to scribble some text?\n")

  drawing = input("\nDid you draw anything today?  Or would you like to share an artwork you relate to today? If yes, share only the file path of the drawing.\n")

  # Writing all the answers into a file.
  # This file will be accessible only for the person.
  # The Therapist view will NOT have access to this file.

  journal_entry = f'''
  ----------------------------------------------------------
  {date_display}

  What emotions did I experience today and why?: {experience}
  Did I learn any insights or lessons from the day?: {lessons}
  What challenges or obstacles did I encounter today, and how did I approach them?: {obstacles}
  What are the key reflections from the day?: {reflections}
  Do you want to share anything else? Write a poem? Have a quote you relate to? Or just want to scribble some text?: {extra}

  Did you draw anything today? Or would you like to share an artwork you relate to today? If yes, share only the file path of the drawing: {drawing}
  '''

  writing_entry_to_file(journal_entry, journal_file)

  print('Thank you for Journaling!! <3')

  """## Analysis

  This is the part where GenAI comes into picture
  """

  def get_entry(file_name):
    if file_name not in os.listdir(data_folder):
      return "", ""

    with open(os.path.join(data_folder, file_name), "r") as f:
      text_in_file = f.read()

    text_entries = text_in_file.split('----------------------------------------------------------')

    if len(text_entries) < 2:
      return text_entries[-1], ""

    return text_entries[-1], text_entries[-2]

  def get_analysis(journal_today, journal_yesterday):

    journal_today_parts = journal_today.split('\n\n')
    journal_yesterday_parts = journal_yesterday.split('\n\n')

    journal_yesterday = journal_yesterday_parts[1] if len(journal_yesterday_parts) > 1 else ''

    journal_prompt = journal_prompt_template.format(journal_today=journal_today_parts[1], \
                                                    journal_yesterday=journal_yesterday)

    journal_model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = journal_model.generate_content(journal_prompt)

    journal_analysis = f'''
  ----------------------------------------------------------
  ### {date_display}

  {response.text}

  '''

    image_name = journal_today_parts[-1].split(':')[-1].replace(' ', '').replace('\n', '')
    if image_name == '' or image_name is None:
      return journal_analysis

    image = PIL.Image.open(image_name)

    drawing_model = genai.GenerativeModel('models/gemini-pro-vision')
    response = drawing_model.generate_content([drawing_prompt_template, image])

    journal_analysis = journal_analysis + f'''

    ## Analysis of the drawing

    {response.text}

    '''

    return journal_analysis

  journal_today, journal_yesterday = get_entry(journal_file)
  analysis_entry = get_analysis(journal_today, journal_yesterday)

  writing_entry_to_file(analysis_entry, analysis_file)

elif user_type == 'T' or user_type == 't':
  """## Therapist View

  This is what the therapist will see about the person.
  """

  def get_analysis_entry(file_name, days_from_today = 0):
    if file_name not in os.listdir(data_folder):
      return [""]

    with open(os.path.join(data_folder, file_name), "r") as f:
      text_in_file = f.read()

    text_entries = text_in_file.split('----------------------------------------------------------')
    text_entries = text_entries[1:]

    if days_from_today < 0:
      return "Please enter a positive number (or 0 for today)"

    if len(text_entries) < days_from_today + 1:
      return "No Entry"

    return text_entries[-1-days_from_today]

  entry_day = input("Please enter the day of the analysis you want to see. 0 - today, 1 - yesterday, and so on...\n")
  analysis_of_the_day = get_analysis_entry(analysis_file, days_from_today=int(entry_day))

  print(analysis_of_the_day)
else:
  print('Invalid input')