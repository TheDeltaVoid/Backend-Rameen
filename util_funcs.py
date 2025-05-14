import hashlib
import flask
import time

cookie_dur = 10

def hash_sha256(inp: str):
    return hashlib.sha256(inp.encode()).hexdigest()

def cookie_resp(user):
    resp = flask.make_response()
    resp.set_cookie("user_id", str(user[0]))
    resp.set_cookie("time", str(time.time()))

    return resp

def cookie_time_refresh_resp():
    resp = flask.make_response()
    resp.set_cookie("time", str(time.time()))

    return resp

def get_cookie():
    id = flask.request.cookies.get("user_id")
    time = flask.request.cookies.get("time")

    if id:
        time = float(time)

        if time + 10 > time.time():
            return int(id)
    
    return False
