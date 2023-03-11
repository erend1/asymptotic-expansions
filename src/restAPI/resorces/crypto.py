from flask import Blueprint, send_file, render_template, url_for, request, redirect
from src.mainAPI.crypto.Crypto import Crypto, Ciphers
from src.utils.Utils import crypto_index_page_params, crypto_index_page_file_reader, get_key_file_path


crypto = Blueprint("crypto", __name__)
key_dict = dict()


@crypto.route(
    rule="/crypto",
    methods=["GET", "POST"],
    endpoint="index"
)
def index():
    if request.method == "POST":
        global key_dict
        language, word, enc_dec, method = crypto_index_page_params(form=request.form)
        if method == "key":
            key, error_flag = crypto_index_page_file_reader(files=request.files)
            print(error_flag)
            if error_flag is not False:
                return redirect(url_for("crypto.index"))
            else:
                key_dict = key
        try:
            word = str(word)
        except ValueError:
            return render_template("/crypto/index.html")

        return redirect(
            url_for(
                'crypto.result',
                language=language,
                word=word,
                enc_dec=enc_dec,
                method=method
            )
        )
    else:
        return render_template("/crypto/index.html")


@crypto.route(
    rule="/crypto/result/<string:language>/<string:word>/<string:enc_dec>/<string:method>",
    endpoint="result"
)
def result(language: str, word: str, enc_dec: str, method: str):
    global key_dict
    crypto_obj = Crypto(language=language)
    cipher_obj = Ciphers(word=word, language=language)

    main_function_dict = {
        "encrypt": crypto_obj.encryption,
        "decrypt": crypto_obj.decryption
    }
    if method == "key":
        A, b = key_dict.values()
    else:
        A, b = cipher_obj.get(key=method)

    main_function_dict[enc_dec](
        word=word, cipher=A, constant=b
    )

    crypto_obj.save_lock_constant()

    key_dict = dict()
    arrays_in_latex = crypto_obj.get_all_arrays_in_latex()

    return render_template(
        "/crypto/result.html", word=crypto_obj.word,
        word_encrypted=crypto_obj.word_encrypted,
        word_arr=arrays_in_latex["word_arr"],
        lock=arrays_in_latex["lock"],
        key=arrays_in_latex["key"],
        constant=arrays_in_latex["constant"],
        encrypted=arrays_in_latex["encrypted"]
    )


@crypto.route(
    rule="/crypto/result/download/<string:file_name>",
    endpoint="download"
)
def download_key_file(file_name):
    path = get_key_file_path(file_name="temp.npz")
    if ".npz" not in file_name:
        file_name = file_name + ".npz"
    if path is None:
        return redirect(url_for("crypto.index"))
    else:
        return send_file(path, as_attachment=True, download_name=file_name)
