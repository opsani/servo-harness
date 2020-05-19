FROM python:3.6-slim
WORKDIR /servo
# Install dependencies
RUN apt update && apt -y install curl
RUN pip3 install requests PyYAML python-dateutil
# Install servo:  batch adjust (which uses the servo base adjust.py) and
# batch measure (which uses the servo base measure.py) and
# servo/state_store used by both measure and adjust
ADD https://raw.githubusercontent.com/opsani/servo/master/servo \
    https://raw.githubusercontent.com/opsani/servo/master/adjust.py \
    https://raw.githubusercontent.com/opsani/servo/master/measure.py \
    https://raw.githubusercontent.com/opsani/servo-vegeta/master/measure \
    ./adjust \
    /servo/
RUN curl -sL https://github.com/tsenart/vegeta/releases/download/v12.8.3/vegeta-12.8.3-linux-amd64.tar.gz| tar xfz - -C /usr/local/bin/
RUN chmod a+x /servo/adjust /servo/measure /usr/local/bin/vegeta
ENV PYTHONUNBUFFERED=1
ENTRYPOINT [ "python3", "servo" ]
