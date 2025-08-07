# Python Keylogger with C2 communication via HTTPS (proof of concept)

## Summary
This project is a simple demonstration of a keylogger with the capability of sending keystrokes via an HTTPS connection. app.py is a simple Flask web app for receiving the keystrokes and dynamically displaying them on the screen using WebSockets. The app also saves all the detected keystrokes in files, with names corresponding to the date of creation, and allows downloading of said files.

## keylogger.py/keylogger
keylogger.py is a simple keylogger written in Python, using the pynput library for capturing keystrokes and requests for sending the keystrokes.  
The listener is responsible for capturing keystrokes and saving them to a global variable delta_data. It is worth mentioning that special characters like Enter and Space will be shown in square brackets, e.g., [ENTER].
<img width="501" height="333" alt="obraz" src="https://github.com/user-attachments/assets/9c3e662c-bd5e-408c-abc0-720f11bd0ff5" />

The sender is responsible for actually sending the captured keystrokes to the C2 server via HTTPS. By default, it sends them every 10 seconds, but that can easily be adjusted by changing the `wait` variable. Lower values lead to a more real-time picture but might cause higher data loss.
<img width="676" height="303" alt="obraz" src="https://github.com/user-attachments/assets/d68831eb-38b0-427c-ba2c-520e9cdfdb3f" />

The current script includes the line:
`urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)`  
This is only here because, during testing, I was using a self-signed certificate, so the line was added to stop the script from constantly writing errors about untrusted TLS.  
The keylogger binary was created using PyInstaller for Linux systems. Surprisingly, it was not detected by my personal anti-malware, but to be fair, it is not the most complex malware and would probably be quite easily detectable in a real-world example.

## Webserver/app.py
It is a simple Flask web server acting as a C2 system for receiving collected keystrokes.
The index function handles both receiving and displaying the keystrokes. If it detects a POST request, the sent data is written into a file and then emitted to the WebSocket to dynamically show every new keystroke without needing to refresh the page.  
<img width="558" height="493" alt="obraz" src="https://github.com/user-attachments/assets/e7a2eaa3-49c8-4352-9006-69a5a7a92e43" />

The download function is purely for downloading the requested file, if it exists. The user can choose not to explicitly select a specific date; in that case, the website will automatically download the most recent file.  
<img width="816" height="420" alt="obraz" src="https://github.com/user-attachments/assets/951624ba-8681-431a-9988-368ed6ccdc46" />
