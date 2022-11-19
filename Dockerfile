FROM python:3

WORKDIR /usr/src/app

COPY recs.txt ./
RUN pip install --no-cache-dir -r recs.txt

COPY . .

EXPOSE 8888

CMD [ "python", "./bot.py" ]