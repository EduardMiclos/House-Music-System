from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artist-list')
def artist_list():
    return render_template('artist_list.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug = True)
