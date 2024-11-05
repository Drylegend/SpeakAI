# Instructions



## Setup backend

Change directory into backend

```shell
cd chatbot/backend
```

### Setup virtual environment

Create a Virtual Environment

```shell
python3 -m venv venv
```

Activate Virtual Environment (MAC)

```shell
source venv/bin/activate
```

Activate Virtual Environment (Windows)

```
venv/Scripts/activate
```

Upgrade PIP

```
pip install --upgrade pip
```

### Install Python packages

Install required Python packages

```
pip install google-generativeai python-decouple fastapi "uvicorn[standard]" python-multipart
```
# 1. Install AWS CLI
Download and install AWS CLI:

### powershell
Start-Process -FilePath "https://awscli.amazonaws.com/AWSCLIV2-Windows-x64.msi" -ArgumentList "/quiet" -Wait

### Verify the installation: Open a Command Prompt and type:

cmd
```
aws --version
```
# 2. Configure AWS CLI
Configure AWS CLI:

```cmd
aws configure
```
### You'll be prompted to enter:

AWS Access Key ID

AWS Secret Access Key

Default region name (e.g., us-east-1)

Default output format (e.g., json)

### 3. Create an S3 Bucket
## Create an S3 bucket using AWS CLI:

```cmd
aws s3 mb s3://your-bucket-name
```
### 4. Use AWS Transcribe
## Install Boto3 for AWS Transcribe:

```cmd
pip install boto3

```


### 5. Create Environment Variables

Create your .env file

```shell
touch .env
```

Update your .env file with the following. You can see your .env by typing sudo nano .env or just by clicking on the file if you are in VS Code.

```plain
ELEVEN_LABS_API_KEY=enter-you-key-here
AWS_ACCESS_KEY_ID=enter-you-key-here
AWS_SECRET_ACCESS_KEY=enter-you-key-here
AWS_REGION=enter-you-region-here
GEMINI_API_KEY=enter-you-key-here

```

### Start your backend server

Start your backend server

```shell
uvicorn main:app
```

Alternatively, you can ensure your server resets every time you make a change by typing:

```shell
uvicorn main:app -- reload
```

You can check your server is working by going to:

```plain
http://localhost:8000/health
```

## Setup frontend

Change directory into frontend

```shell
cd ..
cd chatbot/frontend
```

Install packages

```shell
yarn --exact
```

Build application

```shell
yarn build
```

Start server in dev mode

```shell
yarn dev
```

You can check your dev server is working by going to:

```plain
http://localhost:5173/health
```

or alternatively in live mode:

```shell
yarn start
```

You can check your live server is working by going to:

```plain
http://localhost:4173/health
```
