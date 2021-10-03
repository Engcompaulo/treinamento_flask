FROM ubuntu
RUN apt-get update -y && apt-get upgrade -y && apt-get install python -y && apt-get install pip -y &&  apt-get clean 
CMD  mkdir /var/app/
COPY requirements.txt /var/app/
COPY app.py /var/app/
#MD pip install -r /var/app/requirements.txt
CMD pip install flask && pip install typing && pip install tinydb && pip install pydantic && pip install flask_pydantic_spec && cd /var/app/ && FLASK_DEBUG=1 flask run
#CMD FLASK_DEBUG=1 flask run /var/app/app.y
EXPOSE 5000
