from typing import Any, List
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import httpx
from fastapi.middleware.cors import CORSMiddleware
from bot_model.chat import bot_response
from config import settings
from pydantic import env_settings

ENV = env_settings.read_env_file(settings.Config.env_file)
GITHUB_API_ADDRESS = ENV["github_api_address"]
GITBOT_API_NAME = ENV["gitbot_api_name"]
API_VERSION = ENV["api_version"]
GITBOT_API_PREFIX = f"{GITBOT_API_NAME}/{API_VERSION}"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: Any, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get(f"/{GITBOT_API_PREFIX}/repos")
async def get(github_account, token=""):
    async with httpx.AsyncClient(auth=('bearer', token)) as client:
        github_response = await client.get(f'{GITHUB_API_ADDRESS}/users/{github_account}/repos')
        repos = github_response.json()
        repos_number = len(repos)
        forked_repos_number = len([repo for repo in repos if repo["fork"] == True])
        repos.sort(key=lambda repo: datetime.datetime.strptime(repo["updated_at"], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
        recent_repos = [ { "name": repo["name"], "url": repo["html_url"] } for repo in repos[:3]]
        
        repo_info = {
            "total": repos_number,
            "forked": forked_repos_number,
            "own": repos_number - forked_repos_number,
            "recentRepos": recent_repos
        }         

        return repo_info

@app.get(f"/{GITBOT_API_PREFIX}/events")
async def get(github_account, token=""):
    async with httpx.AsyncClient(auth=('bearer', token)) as client:
        github_response = await client.get(f'{GITHUB_API_ADDRESS}/users/{github_account}/received_events')
        events = github_response.json()
        events_number = len(events)
        pr_events_number = len([event for event in events if event["type"] == "PullRequestEvent"])
        create_events_number = len([event for event in events if event["type"] == "CreateEvent"])
        delete_events_number = len([event for event in events if event["type"] == "DeleteEvent"])
        
        event_info = {
            "total": events_number,
            "pullRequest": pr_events_number,
            "createEvent": create_events_number,
            "deleteEvent": delete_events_number
        }        

        return event_info

@app.get(f"/{GITBOT_API_PREFIX}/statistics")
async def get(github_account, token=""):
    async with httpx.AsyncClient(auth=('bearer', token)) as client:
        github_repos_response = await client.get(f'{GITHUB_API_ADDRESS}/users/{github_account}/repos')
        repos = github_repos_response.json()
        repos.sort(key=lambda repo: datetime.datetime.strptime(repo["updated_at"], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
        recent_repos = [ { "name": repo["name"], "url": repo["html_url"] } for repo in repos[:3]]
        
        code_frequency_repos = []
        commit_activity_repos = []
        for repo in recent_repos:
            code_frequency_response = await client.get(f'{GITHUB_API_ADDRESS}/repos/{github_account}/{repo["name"]}/stats/code_frequency')
            commit_activity_response = await client.get(f'{GITHUB_API_ADDRESS}/repos/{github_account}/{repo["name"]}/stats/commit_activity')

            code_frequency_response_json = code_frequency_response.json()

            commit_activity_response_json = commit_activity_response.json()

            total_addition = sum(code_freq[1] for code_freq in code_frequency_response_json)
            total_deletion = sum(code_freq[2] for code_freq in code_frequency_response_json)
            
            code_frequency_repos.append({
                "name": repo["name"],
                "addition": total_addition,
                "deletion": total_deletion
            })
            commit_activity_repos.append({
                "name": repo["name"],
                "activity": [{ "total": act["total"], "week": act["week"] } for act in commit_activity_response_json]
            })
        
        return {
            "codeFrequency": code_frequency_repos,
            "commitActivity": commit_activity_repos
        }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message({
                "client": str(client_id),
                "content": data
            }, websocket)

            bot_resp = bot_response(data)
            tag = bot_resp.get_tag()
            if tag != "reject" and tag != "greeting" and tag != "goodbye" and tag != "thanks":
                await manager.send_personal_message({
                    "client": "bot",
                    "content": bot_resp.get_message(),
                    "action": "get",
                    "tag": tag
                }, websocket)
            else:
                await manager.send_personal_message({
                    "client": "bot",
                    "content": bot_resp.get_message()
                }, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
