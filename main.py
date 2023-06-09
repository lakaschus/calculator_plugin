import json

import quart
import quart_cors
from quart import request
import random

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
_Facts = {0: "Yao Yao's name in Chinese is 姚瑶. It means 'precious jade'. :)",
          1: "Yao Yao's is a passionate piano player. She studied the piano in Germany, at Trossingen and Würzburg conservatories.",
          2: "Yao Yao loves to eat spicy food such as fish in hot chili oil (水煮鱼), and hot pot (火锅).",
          3: "Yao loves to dance and to sing. She has been dancing and singing since she was 2 years old.",
          4: "Yao Yao loves to travel. Her favorite country is Malaysia!",
          5: "Yao loves the opera, like Mozart's 'The Magic Flute' and Puccini's 'Tosca'."}

@app.route("/")
def home():
    return 'API works!'

@app.get("/yaoyao")
async def get_fact_response():
    rand_int = random.randint(0, len(_Facts) - 1)
    fact = _Facts[rand_int]
    return quart.Response(response=json.dumps([fact]), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5005)

if __name__ == "__main__":
    main()
