from flask import request, Flask, jsonify
import json
import execjs
import requests
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/<path:path>', methods=['POST'])
def post_Data(path):
    data1 = json.loads(request.data)
    head = data1['head']
    head['H_SN'] = uuid()
    head['H_TIME'] = timestap1()
    data1['head'] = head
    data2 = post2bank(data1)
    return jsonify(data2), 201
    
def post2bank(data1):
    url = "https://*.com.cn" + request.full_path
    url = url.replace('?','')
    r = requests.post(url= url,data=json.dumps(data1),headers=request.headers)
    print(r.text)
    return(json.loads(r.text))

def uuid():
    # H_SN = 'H_SN'
    uuid1 = execjs.compile("""
    
    function uuid2(){
		var s = [];
		var hexDigits = "0123456789abcdef";
		for (var i = 0; i < 36; i++) {
			s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
		}
		s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
		s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
		s[8] = s[13] = s[18] = s[23] = "-";

		var uuid = s.join("");
		return uuid;
	}
    """)
    H_SN = uuid1.call("uuid2")
    return(H_SN)

def timestap1():
    timestap = time.time()
    timestap = str(timestap).replace('.','')
    return timestap


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
