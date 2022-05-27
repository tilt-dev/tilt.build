import http
import os
import subprocess
import time
from screenshot import Screenshot, Screenshotter

def git_clone(url):
    if not os.path.isdir(os.path.basename(url)):
        subprocess.check_call(["git", "clone", url])

def tilt_wait(args=None, resource=None, timeout=None):
    cmd = ["tilt", "wait"]
    if args:
        cmd.extend(args)
    elif resource:
        cmd.extend(["--for=condition=Ready", "uiresource", resource])
    else:
        cmd.extend(["--all", "--for=condition=Ready", "uiresource"])
    if timeout:
        cmd.extend(["--timeout", timeout])
    subprocess.check_call(cmd)

def tilt_wait_status_ok(resource, update=True, runtime=True, timeout=None):
    if update:
        tilt_wait(["--for=jsonpath={.status.updateStatus}=ok", "uiresource/%s" % resource], timeout=timeout)
    if runtime:
        tilt_wait(["--for=jsonpath={.status.runtimeStatus}=ok", "uiresource/%s" % resource], timeout=timeout)

def tilt_trigger(resource):
    subprocess.check_call(["tilt", "trigger", resource])

def tilt_patch(tiltfile):
    subprocess.check_call(["tilt", "patch", "tiltfile", "(Tiltfile)", "-p", '{"spec":{"path":"%s"}}' % tiltfile])
    tilt_trigger("(Tiltfile)")

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
    # HTML
    Screenshot(
        git_repo="tilt-example-html",
        tiltfile="0-base/Tiltfile",
        filename="example-static-html-image-1.png",
    ),
    Screenshot(
        git_repo="tilt-example-html",
        tiltfile="1-measured/Tiltfile",
        filename="example-static-html-image-2.png",
        wait_for=[lambda: tilt_wait_status_ok("deploy", runtime=False),
                  lambda: tilt_wait_status_ok("example-html")],
    ),
    Screenshot(
        git_repo="tilt-example-html",
        tiltfile="2-recommended/Tiltfile",
        filename="example-static-html-image-3.png",
        wait_for=[lambda: tilt_wait_status_ok("example-html"),
                  lambda: time.sleep(1)],
    ),

    # Go
    Screenshot(
        git_repo="tilt-example-go",
        tiltfile="0-base/Tiltfile",
        filename="example-go-image-1.png",
        wait_for=lambda: tilt_wait(timeout="60s") # first build is slow
    ),
    Screenshot(
        git_repo="tilt-example-go",
        tiltfile="1-measured/Tiltfile",
        filename="example-go-image-2.png",
        wait_for=[lambda: tilt_wait(),
                  lambda: tilt_wait_status_ok("deploy", runtime=False),
                  lambda: time.sleep(0.5),
                  lambda: tilt_wait_status_ok("example-go")],
    ),
    Screenshot(
        git_repo="tilt-example-go",
        tiltfile="2-optimized/Tiltfile",
        filename="example-go-image-3.png",
        wait_for=[lambda: tilt_wait(),
                  lambda: time.sleep(1),
                  lambda: tilt_wait_status_ok("deploy", runtime=False),
                  lambda: tilt_wait_status_ok("example-go-compile", runtime=False),
                  lambda: tilt_wait_status_ok("example-go"),
                  lambda: tilt_wait()],
    ),
    Screenshot(
        git_repo="tilt-example-go",
        tiltfile="3-recommended/Tiltfile",
        filename="example-go-image-4.png",
        restart=True,
        wait_for=[lambda: tilt_wait(),
                  lambda: tilt_wait_status_ok("example-go"),
                  lambda: time.sleep(1),
                  lambda: tilt_trigger("deploy"),
                  lambda: time.sleep(1),
                  lambda: tilt_wait()],
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

    if tilt and screenshot.restart:
        tilt.terminate()
        tilt = None

    if not tilt:
        tilt = tilt_up(tiltfile)
    elif previous_tiltfile:
        tilt_patch(tiltfile)

    time.sleep(0.25)             # give a little time for Tiltfile to evaluate

    if len(screenshot.wait_for) > 0:
        for action in screenshot.wait_for:
            action()
    else:
        tilt_wait()

    screen.take_screenshot(screenshot)
    previous_tiltfile = tiltfile

tilt.terminate()
screen.close()
