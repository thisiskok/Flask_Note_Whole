FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5001

# Set environment variable to specify the Flask app
ENV FLASK_APP=website:create_app

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

