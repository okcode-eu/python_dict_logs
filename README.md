# python_dict_logs
A simple example on how to play with python's logging module.

This is the result of a few hours of reading about logging module and an unsuccessful attempt to introduce structlog into one of my projects. I realized I just need to add some data to every log, things like thread id, request id, without adding those to every log.debug call. Also, it seems to be useful to add some extra data to selected logs. Ok. You can do it by just adding "%s" and an extra parameter. But what if I wanted to json format it or do any other transformation? Well, this is why I tried to use structlog after all, but it seemed to me overly complicated and unfinished. So here we are with the simple few line of code.
