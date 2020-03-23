FROM python:3
RUN apt-get update && \
	apt-get install -y cron && \
	echo "0 11 * * * python /get_data.py" >> /etc/crontab 
COPY . /
RUN pip install -r requirements.txt
CMD [ "./run.sh" ]
