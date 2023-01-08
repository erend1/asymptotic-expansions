from flask import Flask
from src.utils.Utils import get_logger
from src.restAPI.resorces import series, sequences, crypto


app = Flask(
    __name__,
    template_folder="restAPI/build/templates",
    static_folder="restAPI/build/static"
)

logger = get_logger()

api_version = "/api/v1"

app.register_blueprint(series.series, url_prefix=api_version)
app.register_blueprint(sequences.sequences, url_prefix=api_version)
app.register_blueprint(crypto.crypto, url_prefix=api_version)


def run():
    logger.info("Rest server is started...")
    app.run()


if __name__ == "__main__":
    run()
