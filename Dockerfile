FROM python:3

RUN pip install --upgrade pip

RUN python -m pip install git+https://github.com/kksgandhi/java-format-like-python

ENTRYPOINT ["j2p-fmt"]
