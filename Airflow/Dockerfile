FROM apache/airflow:2.7.0

USER root

# Install dependencies required for Chrome and chromedriver
RUN apt-get update \
    && apt-get install -y --no-install-recommends vim wget unzip gnupg2 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    # Replace the dynamic CHROMEDRIVER_VERSION fetching with a specific version
    && wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip" \
    && unzip /chromedriver/chromedriver* -d /usr/local/bin/ \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /chromedriver

COPY requirements.txt /

USER airflow

RUN pip install --user -r /requirements.txt

