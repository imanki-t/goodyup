FROM python:3.9-slim

# Step 1: Install basic system tools required for the build
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Step 2: Install Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Setup Python Environment
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy Code and Start
COPY . .

# Port for Render Health Check
EXPOSE 10000

CMD ["python", "bot.py"]
