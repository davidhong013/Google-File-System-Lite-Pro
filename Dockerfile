# Step 1: Start with an official Python runtime as a base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any necessary dependencies using apt-get
RUN apt-get update && apt-get install -y grpcio-tools && apt-get clean

# Step 5: Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the ports your services will use
EXPOSE 50051

# Step 7: Set ENTRYPOINT to allow flexibility in running different services
ENTRYPOINT ["python", "-m"]

# Step 8: Set default CMD to start `gfs-master`
CMD ["gfs-master", "gfs.master_server.master_main:serve"]
