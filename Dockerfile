FROM python:3.5

# Install python and pip
ADD ./web/requirements/base.txt /tmp/base.txt
ADD ./web/requirements/production.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -r /tmp/requirements.txt

# Add our code
ADD ./web /opt/webapp/
WORKDIR /opt/webapp
ENV DJANGO_SETTINGS_MODULE=configurations.settings.production
ENV DJANGO_SECRET_KEY='ynozdacxox8=yt*o9+m#6*371a1+x_t2)lsff%j-59vlv#ityz'
RUN python manage.py collectstatic

# Expose is NOT supported by Heroku
# EXPOSE 5000 		

# Run the image as a non-root user
RUN adduser --disabled-password myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 

