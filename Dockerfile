# Step 1: Start with an official Python runtime as a base image

FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install necessary Python packages using pip (including grpcio-tools)
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 setup.py install

# Step 5: Expose the ports your services will use (change these if necessary)
EXPOSE 50051

# Step 6: Set ENTRYPOINT to allow flexibility in running different services
ENTRYPOINT ["python", "-m"]

# Step 7: Set default CMD to start `gfs-master`
CMD ["gfs-master", "gfs.master_server.master_main:serve"]

