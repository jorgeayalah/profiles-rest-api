# Use the base Ubuntu Bionic image
FROM ubuntu:bionic


RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates curl gnupg postgresql-client && rm -rf /var/lib/apt/lists/*

RUN echo 'deb http://ppa.launchpad.net/osmadmins/ppa/ubuntu bionic main\n\
deb-src http://ppa.launchpad.net/osmadmins/ppa/ubuntu bionic main' > \
    /etc/apt/sources.list.d/osmadmins-ppa.list

RUN apt-key adv --keyserver keyserver.ubuntu.com \
    --recv A438A16C88C6BE41CB1616B8D57F48750AC4F2CB


# Update package lists and install required packages
RUN apt-get update && \
    apt-get install -y python3-venv zip && \
    rm -rf /var/lib/apt/lists/*


# Set environment variables
ENV PYTHON_ALIAS_ADDED="alias python='python3'"

# Expose port 8000 (assuming you want to expose it)
EXPOSE 8080


# # Set the working directory
# WORKDIR /server.htm

# Copy application files into the container
COPY . .

# Define the command to run your application
CMD ["python3", "hello.py"]