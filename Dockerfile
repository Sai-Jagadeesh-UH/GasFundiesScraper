FROM python:3.12-slim-bullseye

# Set work directory
WORKDIR /app

# Copy files into container
COPY . src/

# RUN pip install --upgrade pip
# Install Python dependencies
RUN pip install --no-cache-dir -r src/requirements.txt

# Install Playwright Chromium dependencies
RUN apt-get update && apt-get install -y wget curl gnupg && apt-get clean

RUN curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb

RUN dpkg -i packages-microsoft-prod.deb

RUN rm packages-microsoft-prod.deb

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install Chromium only
RUN playwright install chromium

# WORKDIR /app/src/playwright
# Expose your app's port
# DontAskMeAgain@123DontAskMeAgain@123
EXPOSE 5085

# Run via Gunicorn in production (update 'app:app' if your entry point is different)
# CMD ["gunicorn", "--bind", "0.0.0.0:5085", "main:app"]