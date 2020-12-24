FROM python:3.7

COPY ./ .
WORKDIR "requirements/mindmeld/"
RUN python setup.py install 
WORKDIR ../..
RUN pip install -r requirements.txt
RUN mindmeld
# specify the port number the container should expose
EXPOSE 8000
ENTRYPOINT [ "python" ]

CMD ["flask_app.py"]