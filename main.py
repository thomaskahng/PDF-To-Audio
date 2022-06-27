from flask import Flask, render_template, request, redirect, url_for
import PyPDF2
import pyttsx3
import pikepdf

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/say", methods=['GET', 'POST'])
def say():
    if request.method == 'POST':
        # Get PDF name
        pdf_input = str(request.form.get("thing"))
        pdf_name = f"{pdf_input}.pdf"

        # Extract file and save in new file
        pdf = pikepdf.open(pdf_name)
        pdf.save('extractable.pdf')

        try:
            # Open filepath and file read object
            path = open('extractable.pdf', 'rb')
            pdfReader = PyPDF2.PdfFileReader(path)
            numPages = pdfReader.getNumPages()

            for i in range (0, numPages):
                # Start all text from page 1
                from_page = pdfReader.getPage(i)
                text = from_page.extractText()

                # Speak the text and wait until everything is said
                speak = pyttsx3.init()
                speak.say(text)
                speak.runAndWait()

        # If error do nothing
        except:
            return redirect(url_for("home"))

        return redirect(url_for("home"))

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)