from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None]


    def to_dict(self):
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete":self.completed_at if self.completed_at else False
        }
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
        description= task_data["description"],
        completed_at = None if not task_data.get("is_complete") else task_data.get("is_complete"))
        return new_task
        

    