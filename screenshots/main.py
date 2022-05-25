import http
import os
import subprocess
import time
from screenshot import Screenshot, Screenshotter

def git_clone(url):
    if not os.path.isdir(os.path.basename(url)):
        subprocess.check_call(["git", "clone", url])

def tilt_wait():
    time.sleep(0.5)             # give a little time for Tiltfile to evaluate
    subprocess.check_call(["tilt", "wait", "--all", "--for=condition=Ready", "uiresource"])

def tilt_patch(tiltfile):
    subprocess.check_call(["tilt", "patch", "tiltfile", "(Tiltfile)", "-p", '{"spec":{"path":"%s"}}' % tiltfile])
    subprocess.check_call(["tilt", "trigger", "(Tiltfile)"])

def tilt_up(tiltfile):
    tilt = subprocess.Popen(["tilt", "up", "--legacy=false", "--stream=true", "-f", tiltfile])
    connected = False
    for i in range(10):
        conn = http.client.HTTPConnection("localhost", 10350)
        try:
            conn.request("HEAD", "/")
            resp = conn.getresponse()
            if resp.status == 200:
                connected = True
                break
        except ConnectionRefusedError:
            pass
        conn.close()
        time.sleep(1)

    if not connected:
        print("Timed out waiting for Tilt to start")
        sys.exit(1)

    return tilt

def tilt_down(tiltfile):
    subprocess.check_call(["tilt", "down", "-f", tiltfile])

screenshots = [
    Screenshot(
        git_repo="tilt-example-html",
        tiltfile="0-base/Tiltfile",
        filename="example-static-html-image-1.png",
    ),
    Screenshot(
        git_repo="tilt-example-html",
        tiltfile="1-measured/Tiltfile",
        filename="example-static-html-image-2.png",
    ),
    Screenshot(
        git_repo="tilt-example-html",
        tiltfile="2-recommended/Tiltfile",
        filename="example-static-html-image-3.png",
    ),
]

screen = Screenshotter()
previous_tiltfile = None
tilt = None

for screenshot in screenshots:
    if previous_tiltfile and not previous_tiltfile.startswith(screenshot.git_repo):
        tilt.terminate()
        tilt = None
        tilt_down(tiltfile)

    git_clone("https://github.com/tilt-dev/%s" % screenshot.git_repo)
    tiltfile = "%s/%s" % (screenshot.git_repo, screenshot.tiltfile)

    if not tilt:
        tilt = tilt_up(tiltfile)
    elif previous_tiltfile:
        tilt_patch(tiltfile)

    tilt_wait()
    screen.take_screenshot(screenshot)
    previous_tiltfile = tiltfile

tilt.terminate()
screen.close()
