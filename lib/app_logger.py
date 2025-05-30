import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s : %(message)s',
                    handlers=[logging.FileHandler("app.log", encoding='utf-8'),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)
