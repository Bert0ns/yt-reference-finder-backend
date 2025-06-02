import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s : %(message)s',
                    handlers=[logging.FileHandler("app.log", encoding='utf-8'),
                              logging.StreamHandler()])

logger = logging.getLogger(__name__)


def trim_log_file(max_lines=5000):
    """
    Trims the log file to keep only the last `max_lines` lines.
    """
    try:
        with open("app.log", "r+", encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > max_lines:
                f.seek(0)
                f.writelines(lines[-max_lines:])
                f.truncate()
                logger.info(f"Log file trimmed to last {max_lines} lines.")
            else:
                logger.info("Log file does not need trimming.")
    except Exception as e:
        logger.error(f"Error trimming log file: {e}")