from flask import Flask, render_template, request, redirect
import speech_recognition as sr

app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods = ['GET', 'POST'])

def index():
    transcript = ''
    
    def handle_submit(request):
        # If this function is placed outside index, there seems to be an error (related to scopes, names clashes, maybe?)
        # I'd like to figure that out later.

        if 'file_name' not in request.files:
            # would be nice to display something here
            print("not there")
            return redirect(request.url)
        file = request.files['file_name']
        if not file or file.filename == '':
            print("blank name")
            return redirect(request.url)

        recog = sr.Recognizer()
        audio_file = sr.AudioFile(file)
        with audio_file as af:
            data = recog.record(af)
        transcript = recog.recognize_google(data, key=None)
        return transcript
        
    if request.method == 'POST':
        # Form submitted.
        transcript = handle_submit(request)
        if type(transcript) != str: transcript = ''
        
    return render_template('index.html', transcript=transcript) # Flask looks into the templates folder automatically.

if __name__ == '__main__':
    app.run(debug=True, threaded=True, extra_files='C:\\Users\\mouss\\Documents\\small_projects\\speech-recog\\templates\\index.html')
    # The debug option allows to page to refresh without restarting the server.
    # You can also specify the port here.
    # Still trying to figure out how to detect changes and RE-RENDER when the template file changes.
    # So far, extra_files and TEMPLATES_AUTO_RELOAD don't work.
    # Might take a look at jinja or livereload.
