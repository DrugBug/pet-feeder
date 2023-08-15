import logging
from settings import WEBSERVER_PORT
from webserver import app
from imp import reload

reload(logging)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=WEBSERVER_PORT, debug=True)
