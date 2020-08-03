# flash playground
from flask import Flask , request, url_for ,render_template ,jsonify, send_file, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# elasticsearch playground
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# method create for elasticsearch
import esMethod

#Default server online
@app.route('/', methods = ["GET", "POST"])
def helloworld():
    print("Sever Online")
    return 'Server Online'

# @app.route('/index',methods=['POST'])
# def index():
#         json_file = request.json
#         print(json_file)
#         esMethod.index(client=es,index="patient",json_dict=json_file)
#         return 'Reviewer created'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555)