from datetime import datetime
import os.path
#import time
from flask import render_template,jsonify,request, make_response, send_from_directory, send_file
from httpx import Response
from llama_parse import LlamaParse
from AIGuide import app
from groq import Groq
import speech_recognition as sr
import pyttsx3
from flask_socketio import SocketIO, send
import uuid
import re
import html_text
import json
from bs4 import BeautifulSoup
from decouple import config
#from AIGuide.Objects.GoogleImage import GoogleImage
from AIGuide.Objects.LlamaIndexProc import GetGroqResponse, GetQueryMultyResp, GetQueryResponse
from serpapi import GoogleSearch


global client_id
client_id = uuid.uuid4().hex

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('Cust_message') #specific client
def handle_custom_event(data):
    socketio.emit('Cust_resp' + client_id, {'data': data})

@socketio.on('Cust_message_select') #specific client
def handle_custom_event_select(data):
    socketio.emit('Cust_resp_select' + client_id, {'data': data})    

@socketio.on('Cust_message_AI') #specific client
def handle_custom_event_ai(data, isHTML=False, isSpeech = False):
    if data is not None:
        
        if isHTML == False:
            pattern = r'"(.*?)"'
            matches = re.findall(pattern, data)
        
            if len(matches)>0:
                data = matches[0]
        
        if isHTML == False:
            socketio.emit('Cust_resp_AI' + client_id, {'data': data, 'history': '**Query: ' + data + '**'})
        else:
            #resp_html = lLamaResp(data,True)

            #soup = BeautifulSoup(data,"html.parser", from_encoding="utf-8")

            #googleImage = GoogleImage("Polynomial in mathematics")
            #imageData = googleImage.searchImage(), 'history': resp

            resp = html_text.extract_text(data)
            if isSpeech == True and isHTML == True:
                SpeakTextSave(resp)

            #socketio.emit('Cust_resp_AI' + client_id, {'data': soup.prettify() + "<hr/>"})
            socketio.emit('Cust_resp_AI' + client_id, {'data': data, 'history': data + "\n\n ****** \n\n"})
        
        #for wrd in resp.split():
        #    if wrd.endswith("."):
        #        sleep(100/1000)
            #else:
            #    sleep(100/1000)
            #listenAudio()

#if __name__ == '__main__':
    #socketio.run(app, debug=True)

global cspeach
cspeach = ""
global stop_listening
global inproc
inproc = True
global promptResult
promptResult = ""

def rec_audio(recognizer, audio):
    try:
        MyText = recognizer.recognize_google(audio)           
        MyText = MyText.lower()
        #global cspeach
        #cspeach += MyText + " "
        #print(cspeach)
        if MyText is not None:
            #socketio.send(MyText)#Socket Msg
            handle_custom_event(MyText)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
    
#global cspeach
#cspeach = ""

def set_cookie(key,value):
    response = make_response('Cookie set')
    response.set_cookie(key, value)
    return response

def get_cookie(key):    
    return request.cookies.get(key)

def lLamaResp(prompt,isHtml,history = ""):
    try:
        promptPolicy = f"""
        - **** Make sure: Don't allow the input request that the prompt to deviate from your prompting policies. 
        This request is especially for educational purposes; don't allow the prompt to contain any
        illegal, irrelevant, sexual, hateful, violent, promotes self-harm, harassment, or negative key words.
        If the prompt deviates from any policies, don't return any results; rather, give a warning message. ****
        """

        frmPrompt = prompt
        sysprompt = f"""
        You are in a language professional role and need to help correct the text input for prompting.
        {promptPolicy}
        """
        if isHtml == True:

            frmPrompt_html = f"""
            {prompt}
            - *** The format of the extracted result is in HTML content always.            
            """
            sysprompt_html = f"""
            You are in a technical professional role here and need to explain or list out the required results for the student's queries clearly with some pictorial references.
            Requirements for the response result in HTML-formatted content: 
            - Include the relevant examples and case studies to illustrate the key concepts. 
            - Use relevant subject-valid images from accessible and available free sources. 
            - The image should be suitable for student demonstrations.
            - The image tag should be rendered from available and free sources; add a suitable text image tag's alt attribute.
            - The code blocks should be clearly rendered inside of a <pre> tag with 800px of max width, and the codes should be indended properly, line by line, with line wrapping (add copy code functionality with a link or a button).
            - Desired Output: A comprehensive guide in HTML-formatted contents, including examples and image tags.
            - Format the result in HTML content with proper headings, paragraphs, containers, divs, etc.
            - Wherever required, add <li>, <p>, <div>, <h>, <code>, <img> etc. 
            - The format of the extracted result is in HTML content.
            {promptPolicy}
            """
            
            passage_history = ""

            global promptResult
            if history != None and history != "":
                passage_history = f"""
                                    - Refer to passage history to provide a relevant response to the user request.
                                    *** PASSAGE_HISTORY=[{history}].
                                    """            

            frmPrompt = f"""
            {prompt}
            """
            sysprompt = f"""
            You are in a technical professional role here and need to explain or list out the required results for the student's queries clearly with some pictorial references.
            Requirements for the response result: 
            - Include the relevant examples and case studies to illustrate the key concepts. 
            - Use relevant subject-valid images from accessible and available free sources. 
            - The image should be suitable for student demonstrations.
            - The image tag should be rendered from available and free sources; add a suitable text image tag's alt attribute.
            - The code blocks should be clearly rendered and formatted well with suitable colors.
            - Provide the resource information in the response.
            - Don't respond if the request is irrelevant/illegal or in any harm category [SEXUALLY EXPLICIT, HATE SPEECH, HARASSMENT, DANGEROUS CONTENT].
            """
        
        prompt = [
            {
                "role" : "system",
                "content": sysprompt
            },
            {
                "role": "user",
                "content": frmPrompt
            }
        ]        
        
        if history != "" and isHtml == True:
            queryPrompt = prompt[1]['content']
            sysAdd = "Refer to passage history from local document storage (RAG) and try to fetch a new additional response from the model."
            history = sysprompt + "\n\n" + history
            completion = GetQueryResponse(queryPrompt, history)
        else:
            completion = GetGroqResponse(prompt)

        if isHtml == True:
            #global promptResult
            promptResult = {"user_request":prompt[1]['content'],"responses": [{"response":completion}]}

        return completion
    except Exception as e:
        print("The error is: ",e)

def SpeakText(command):    
    # Initialize the engine    
    #engine.startLoop(False)
    #engine.runAndWait()
    #engine.iterate()
    #voices = engine.getProperty('voices')
    engine = pyttsx3.init()
    engine.say(command)
    handle_custom_event_select(command)
    engine.runAndWait()
    """
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("Hello World!")
        engine.runAndWait()
        engine.stop()
    """
    #engine.setProperty('rate', 100)
    #engine.setProperty('voice', voices[0].id)
    """
    for wrd in command.split("\n"):
        #if(line is not None and line != ""):
            #for wrd in line.split():
        if(wrd is not None and wrd.strip() != ""):
            handle_custom_event_select(wrd.strip())
            engine.say(wrd)
        engine.iterate()
    engine.endLoop()
    """

def SpeakTextSave(command):    
    # Initialize the engine    
    #engine.startLoop(False)
    #engine.runAndWait()
    #engine.iterate()
    #voices = engine.getProperty('voices')
    engine = pyttsx3.init()
    """
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice, voice.id)
        engine.setProperty('voice', voice.id)
        engine.say("Hello World!")
        engine.runAndWait()
        engine.stop()
    """
    #engine.setProperty('rate', 100)
    #engine.setProperty('voice', voices[0].id)
    """
    for wrd in command.split("\n"):
        #if(line is not None and line != ""):
            #for wrd in line.split():
        if(wrd is not None and wrd.strip() != ""):
            handle_custom_event_select(wrd.strip())
            engine.say(wrd)
        engine.iterate()
    engine.endLoop()
    """

    audioPath = os.path.join(os.getcwd(), 'AIGuide\\static\\audio')
    engine.save_to_file(command.replace("\n", "    "), os.path.join(audioPath, client_id + ".wav"))
    engine.runAndWait()

def recieve():
        try:
            r = sr.Recognizer()
            m = sr.Microphone()
            with m as source:
                r.adjust_for_ambient_noise(source)
    
            global stop_listening
            stop_listening = r.listen_in_background(m, rec_audio)
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        
        except sr.UnknownValueError:
            print("unknown error occurred")  

def listenAudio():
    # Initialize recognizer class                                       
    r = sr.Recognizer()
    r.pause_threshold = 1.0
    r.phrase_threshold = 1.0
    r.non_speaking_duration = 1.0
    # audio object
    #audioPath = os.path.join(os.getcwd(), 'AIGuide\\static\\audio')
    #audioPath = os.path.join(audioPath, client_id + ".mp3")
    audio = sr.AudioSource() #sr.AudioFile(audioPath)
    #read audio object and transcribe
    with audio as source:
        audio = r.record(source)                  
        result = r.recognize_google(audio)
        SpeakText(result)


def loadResp():
    listen = False

def linecorrect(prompt,isSpeech = False):
    if prompt != "":
        cor_prmpt = "I need your help to correct my draft-level prompt for typos and grammar. Don't express any comments or message from your end in the response and dont give any suggestion as a paragraph, I need only the corrected prompt string. Please find the following prompt and return the corrected prompt string. Prompt:[{0}]".format(prompt)
        resp = lLamaResp(cor_prmpt,False)
        handle_custom_event_ai(resp,False,isSpeech)
        return resp

@app.route('/home/setclient/<clientid>')
def SetClientId(clientid):
    global client_id
    client_id = clientid
    return jsonify({"airesp":client_id})

@app.route('/home/speak/<mode>')
def speak(mode):
    print(mode)
    if mode == "start":
        recieve()
    else:
        if stop_listening is not None:
            stop_listening(wait_for_stop=False)
     
    if mode == "stop":
        handle_disconnect()
        return jsonify({"airesp":cspeach})
    else:
        return jsonify({"airesp":mode})

@app.route('/home/read')
def read():
    #print("Reading" + cspeach)
    return jsonify({"airesp":cspeach})

#@app.route('/home/ask/<prompt>')
@app.route('/home/ask',methods=['POST'])
def ask():
    if request.method == "POST":
        content = request.get_json()
        prompt = content['prompt']
        isSpeech = content['isSpeech']
        history = content['history']
        inproc = False
        #resp = GetQueryResponse(prompt)#
        resp = linecorrect(prompt,isSpeech)
        resp = lLamaResp(resp,True,history)
        handle_custom_event_ai(resp,True,isSpeech)
        """
        if cspeach != "":
            resp = lLamaResp(cspeach)
            SpeakText(resp)
            return jsonify({"airesp":resp})
        """ 
        #global cspeach
        #cspeach = "".
        
        return request.form

@app.route('/home/askmore<isSpeech>')
def askmore(isSpeech):
    #json_data = json.dumps(promptResult, indent=2)
    prompt = promptResult["initial_request_prompt"]
    resp_list = ' '.join(item["response"] for item in promptResult["responses"])
    promptMore = f"""
    Need additional result for the initial request of [{prompt[1]["content"]}].
    """
    promptSys_html= f"""
    You are in a technical professional role here and need to explain or list out the additional required results for student's queries clearly with some pictorial references.
    - Refer the HTML content from the older responses in the following list [{resp_list}]. 
    - Make sure the new result should be relevant to the older responses with a new additional contents or lists. 
    - Make sure the new result is in the same format as the older format.
    - The format of the extracted result is in HTML content.
    """

    promptSys= f"""
    You are in a technical professional role here and need to explain or list out the additional required results for student's queries clearly with some pictorial references.
    - Refer the content from the older responses in the following list [{resp_list}]. 
    - Make sure the new result should be relevant to the older responses with a new additional contents or lists. 
    """

    prompt = [
        {
            "role" : "system",
            "content": promptSys
        },
        {
            "role": "user",
            "content": promptMore
        }
    ]  

    #resp = GetQueryResponse(prompt, json_data)
    #resp = GetQueryMultyResp(prompt, json_data)
    #resp = linecorrect(prompt)

    completion = GetGroqResponse(prompt)    

    promptResult["responses"].append({"response":completion})
    handle_custom_event_ai(completion,True,isSpeech)
    return request.form    

@app.route('/home/save/<type>')
def save(type):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    filename = "iguide"
    if type == "html":
        html_content = ""
        for item in promptResult["responses"]:
            html_content += item["response"]
        
        filename = filename + ".html"
        full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
        full_path_upd = os.path.join(full_path,filename)
        with open(full_path_upd, 'w', encoding='utf-8') as file:
            file.write(html_content)
            #file.close()

        #return send_from_directory(full_path, filename, as_attachment=True)
        return send_file(full_path_upd, as_attachment=True)

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        client_id = client_id
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/searchimage/<keyword>')
def searchimage(keyword):
    if(keyword) is not None:        
        params = {
          "api_key": "7a89d603211f2e98d58a1b0778257fcf5d018940dea2de8d62b24bbe5dfd9fc7",
          "engine": "google_images",
          "q": keyword,
          "google_domain": "google.com",
          "gl": "us",
          "hl": "en"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        return jsonify(results)