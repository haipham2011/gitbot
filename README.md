# Gitbot project
This project purpose is to create a chatbot which support user to collect information from his/her github account

<img src="images/Gitbot-demo.gif"/>

# Requirements
- Python 3.9
- virtualenv
- Node v16

# How to start

## Create virtual environment

Create a virtual environment `venv` by:

```
virtualenv -p python3 .venv
```

Install the python dependencies:

```
pip install -r requirements.txt
```
## Train the model

First, we have to produce a model stored in `data.pth` binary file by this command:

```
cd gitbot-model && python train.py
```
The model module is copied and modified based on this [repo](https://github.com/python-engineer/pytorch-chatbot)

## Start the backend
Go to backend directory

```
cd gitbot-api
```

Create an `.env` file with this format:
```
GITHUB_USER = <YOUR_GITHUB_ACCOUNT>
GITHUB_API_ADDRESS = "https://api.github.com"
GITBOT_API_NAME = "gitbot-api"
API_VERSION = "v1"
```

Start the server by:
```
uvicorn main:app --reload
```

## Start the frontend

From rootdir, Go to backend directory:
```
cd gitbot-frontend
```

Create an `.env` file with this format:
```
VITE_BACKEND_HOST=127.0.0.1
VITE_BACKEND_PORT=8000
VITE_API=gitbot-api
VITE_API_VERSION=v1
```

Install dependencies and start
```
npm install
npm run dev
```

# References
1. [Fast API with Python](https://fastapi.tiangolo.com/)
2. [How to build your own chatbot](https://github.com/python-engineer/pytorch-chatbot)
3. [Build frontend with Svelte](https://kit.svelte.dev/)
4. [Tailwind chatbot UI example](https://larainfo.com/blogs/tailwind-css-chat-ui-example)
