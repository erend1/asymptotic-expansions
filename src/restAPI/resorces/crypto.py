import json
from flask import Blueprint, Response, render_template, url_for, request
from src.mainAPI.Crypto import Crypto, Ciphers
from src.utils.Utils import crypto_index_page_params
crypto = Blueprint("crypto", __name__)
main_crypt = Crypto()


@crypto.route(
    "/crypto", methods=["GET", "POST"], endpoint="index"
)
def index():
    if request.method == "POST":
        word, enc_dec, method, A, b = crypto_index_page_params(form=request.form)
        if word is None:
            return render_template("index.html")

        main_cipher = Ciphers(word=word)
        if enc_dec == "decrypt":
            main_function = main_crypt.decryption
        else:
            main_function = main_crypt.encryption

        if method is not None:
            A, b = main_cipher.get(key=method)

        main_function(word=word, cipher=A, constant=b)
        result = main_crypt.get_all_params()
        result = json.dumps(result, indent=4, ensure_ascii=False)
        response = Response(result, mimetype="application/json", status=200)
        return response
    else:
        return render_template("index3.html")

