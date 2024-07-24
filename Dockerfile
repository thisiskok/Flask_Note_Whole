FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5001

CMD [ "python3", "-m" , "flask",  "--app=main", "run", "--host=0.0.0.0"]