from flask import Flask
from src.utils.Utils import get_logger
from src.restAPI.resorces import series, sequences


app = Flask(__name__)

logger = get_logger()

api_version = "/api/v1"

app.register_blueprint(series.series, url_prefix=api_version)
app.register_blueprint(sequences.sequences, url_prefix=api_version)


def run():
    logger.info("Rest server is started...")
    app.run()
