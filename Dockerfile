# our base image
FROM python:3.10.1 

# its where our commands will run and files will be copy in this dir in our container
WORKDIR /usr/src/app

# copy our requirement.txt file to this directory (workdir means => "./")
COPY requirements.txt ./

# installing our requirements there (workdir means => "./")
RUN pip install --no-cache-dir -r requirements.txt

# coppy all our project files from our directory to wokdir directory (workdir means => "./") in container
COPY . .

# runing the comamnd to run our app 
CMD ["uvicorn", "app.main_4:app", "--host", "0.0.0.0", "--port", "8000"]