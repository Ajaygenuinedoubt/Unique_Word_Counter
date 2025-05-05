from flask import Flask, render_template, request, send_file
from collections import Counter
import re
import csv
import io

app = Flask(__name__)

# Global variable to hold word count
word_count_global = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    global word_count_global
    word_count = {}
    if request.method == 'POST':
        text = request.form.get('text_area', '')
        cleaned_text = re.sub(r'[^\w\s]', '', text).lower()
        words = cleaned_text.split()
        word_count = dict(Counter(words))
        word_count_global = word_count  # Save for download
    return render_template('index.html', word_count=word_count)

@app.route('/download')
def download_csv():
    global word_count_global
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Word', 'Count'])
    for word, count in word_count_global.items():
        writer.writerow([word, count])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        download_name='word_count.csv',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
