import time
from sys import platform
from selenium import webdriver
from gologin import GoLogin
from selenium.webdriver.chrome.service import Service
from flask import Flask, render_template, request
from plyer import notification

# Initialize the GoLogin instance
gl = GoLogin({
    "token": "your token",
    "profile_id": "your profile id"
})

app = Flask(__name__)

def clear_cookies(driver):
    driver.delete_all_cookies()

if platform == "linux" or platform == "linux2":
    chrome_driver_path = "./chromedriver"
elif platform == "darwin":
    chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
    chrome_driver_path = "chromedriver.exe"


@app.route('/cookie', methods=['POST'])
def cookie():
    site_url = request.form['site_url']
    delay = int(request.form['delay'])
    closing = int(request.form['closing'])
    debugger_address = gl.start()
    service = Service(executable_path=r'C:\Users\DELE\Downloads\chromedriver_win32\chromedriver.exe')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(site_url)
    start_time = time.time()

    while (time.time() - start_time) < closing:
        clear_cookies(driver)
        notification.notify(
            title='Cookie Cleared',
            message='A cookie has been cleared.',
        )

        time.sleep(delay)
        driver.get(site_url)

    driver.quit()
    time.sleep(5)
    gl.stop()

    return render_template('main.html')


@app.route('/')
def main():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
