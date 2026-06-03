import json
import os

from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core import messages
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from typing import Sequence


#def get_history(session_id):
 #   return FileChatMessageHistory(session_id, " ./chat_history")
def get_history(session_id):
    file_path = os.path.join("./chat_history", f"{session_id}.json")
    return FileChatMessageHistory(file_path)

class FileChatMessageHistoryStore(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, self.session_id)

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(message)for message in all_messages]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)



    @property
    def message(self)-> list[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                message_data = json.load(f)
                return messages.from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)