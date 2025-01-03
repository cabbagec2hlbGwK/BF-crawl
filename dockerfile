from ubuntu

WORKDIR /app/master
RUN apt update
RUN apt install python3  -y
RUN apt install python3-flask -y
RUN apt install python3-requests -y
RUN apt install python3-openai -y
RUN apt install python3-pillow -y
RUN apt install python3-opencv -y
RUN apt install python3-docker -y
ENV OPENAI_API_KEY=""
ENV CONTAINER_NAME=""
ENV BF_CREDS=""
COPY . .

CMD ["bash", "-c", "/app/master/run.sh"]
