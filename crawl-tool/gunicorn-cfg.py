import multiprocessing

bind = '0.0.0.0:5005'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 0
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True