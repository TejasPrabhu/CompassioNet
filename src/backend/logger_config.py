import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Set the level of logger
logger.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("file.log")

c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
format_string = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s in %(filename)s:%(lineno)d"
)
c_format = logging.Formatter(format_string)
f_format = logging.Formatter(format_string)

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
