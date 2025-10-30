from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]


    def to_dict(self):
        is_complete = True if self.completed_at else False
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete":is_complete
        }
    
    def from_dict(self, task_dict):
        self.title = task_dict.get("title")
        self.description = task_dict.get("description")
        self.completed_at = None if task_dict is False else task_dict.get("is_complete")