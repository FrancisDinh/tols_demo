import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, NamedTuple, Optional

from openai import ChatCompletion

from utils import wrapped


DEFAULT_MODEL = "gpt-3.5-turbo"

class StrEnum(str, Enum):
    pass

class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class Message(NamedTuple):
    role: Role
    content: str

    def to_dict(self):
        return {"role": str(self.role), "content": self.content}


class Chat:
    def __init__(
        self,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    )-> None:
        self.model = model if model else DEFAULT_MODEL
        self.temperature = temperature
        self._messages: list[Message] = []
        if system_prompt:
            self._messages.append(Message(Role.SYSTEM, system_prompt))

    def messages(self) -> list[dict[str, str]]:
        return [message.to_dict() for message in self._messages]

    def dict(self) -> dict[str, Any]:
        return {"model": self.model, "temperature": self.temperature, "messages": self.messages}

    def json(self) -> str:
        return json.dumps(self.dict(), indent=2)

    def save_to_file(self, filename: Optional[str] = None) -> None:
        filename = filename if filename else f"chat-{datetime.now().isoformat()}.json"
        path = Path.cwd() / "chat_history" / filename

        path.parent.mkdir(exist_ok=True)

        with path.open(mode="w") as f:
            f.write(self.json())

        print(f"Saved chat to {path}")
        
    def wordcount(self) -> int:
        return sum(len(message.content) for message in self._messages)

    def from_file(cls, file_path: str) -> "Chat":
        with open(file_path, "r") as f:
            state = json.load(f)

        c = cls(model=state["model"], temperature=state["temperature"])
        c._messages = [Message(**message) for message in state["messages"]]
        return c

    def _get_chat_response(self) -> str:
        r = ChatCompletion.create(
            model=self.model, messages=self.messages, temperature=self.temperature, n=1
        )
        return r["choices"][0]["message"]["content"]

    def get_response(self, content: str) -> None:
        self._messages.append(Message(Role.USER, content))

        response = self._get_chat_response()
        self._messages.append(Message(Role.ASSISTANT, response))

        return(response)
