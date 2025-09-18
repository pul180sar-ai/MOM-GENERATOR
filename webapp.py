import google.generativeai as genai
import os 
import streamlit as st
from pdfextractor import text_extractor
from docxextractor import text_extractor_docx
from imageextractor import extract_text_image

# Configure the  Model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model =genai.GenerativeModel('gemini-2.5-flash-lite')


# Upload file in Sidebar
user_text = None
st.sidebar.title(':orange[Upload your MOM notes here: ]')
st.sidebar.subheader("Only Upload Images, PDF's and DOCX")
user_file = st.sidebar.file_uploader("Upload your file",type=['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type =='application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text= text_extractor_docx(user_file)
    elif user_file.type in ['image/jpg','image/jpeg','image/png']:
        user_text = extract_text_image(user_file)
    else:
        st.sidebar.error('Upload Correct File Format')

# Main page 
st.title(':blue[Minutes of Meeting]: :green[AI assisted MoM generator in a standardized form from meeting notes]')
tips ='''Tips to use this app:
* Upload your meeting in side bar (Image,PDF or DOCX)
* Click on generate MoM and get the standardized MoM's'''
st.write(tips)

if st.button('Generate MoM'):
    if user_text is None:
        st.error('Text is not generated')
    else:
        with st.spinner('Processing you data....'):
            prompt =f'''Assume you are expert in creating minutes of meeting. User has provided
            notes of meeting in text format. Using this data you need to create a standardized
            minutes of meeting for the user. 

            Output must follow word/docx format, strictly in the following manner:
            title : Title of meeting
            Heading : Meeting Agenda
            subheading : Name of attendees (If attendess name is not there keep it NA)
            subheading: date of meeting and place of meeting (place means name of conference /meeting room if not provided) 
            Body: The body must follows the following sequence of points
            * Key points discussed
            * Highlight any decision that has been fianlised.
            * mention actionable items.
            * Any additional notes.
            * Any deadline that has been discussed.
            * 2 to 3 line of summary.  
            * Use bullet points and highlight or bold important keywords such the context is clear.
            * Generate the output in such a format that it can be copied and paste in word

            The data provided by user is as follows {user_text} '''

            response =model.generate_content(prompt)
            output = response.text
            st.write(output)

            st.download_button(label='Click To Download ',
                               data= response.text,
                               file_name='MoM.txt',
                               mime='text/plain')
            