from flask import Flask, render_template_string
import datetime, platform, os

app = Flask(__name__)

@app.route('/')
def system_info():
    now = datetime.datetime.now()
    try:
        user = os.getlogin()
    except OSError:
        user = "N/A (e.g., Docker env)"
    
    sys = platform.uname()
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>System Info</title>
    <style>body{font-family:Arial,sans-serif;padding:20px;max-width:600px;margin:auto}
    h1{text-align:center;color:#0056b3}table{width:100%;border-collapse:collapse}
    td{padding:8px;border-bottom:1px solid #eee}</style>
    </head>
    <body>
    <h1>System & Server Info</h1>
    <table>
        <tr><td>Current Time</td><td>{{t}}</td></tr>
        <tr><td>Current Date</td><td>{{d}}</td></tr>
        <tr><td>Hostname</td><td>{{h}}</td></tr>
        <tr><td>OS</td><td>{{os}}</td></tr>
        <tr><td>OS Release</td><td>{{rel}}</td></tr>
        <tr><td>Machine</td><td>{{m}}</td></tr>
        <tr><td>Current User</td><td>{{u}}</td></tr>
    </table>
    </body>
    </html>
    """, t=now.strftime("%H:%M:%S"),
        d=now.strftime("%Y-%m-%d"),
        h=sys.node,
        os=sys.system,
        rel=sys.release,
        m=sys.machine,
        u=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
