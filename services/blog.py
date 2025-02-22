import os
import uuid
from pathlib import Path
from typing import List

from fastapi import UploadFile

from common.constant import STATIC_DIR_NAME
from models import Blog
from services.base import BaseService


class BlogService(BaseService):
    def get_all_blogs(self) -> List[Blog]:
        result = self.session.query(Blog).all()
        return result

    def delete_blog(self, blog_id: uuid.UUID):
        self.session.query(Blog).filter(Blog.id == blog_id).delete()

    def save_image(self, file: UploadFile) -> str:
        file_extension = os.path.splitext(file.filename)[-1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        folder_path = os.path.join(STATIC_DIR_NAME, "images")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, unique_filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return file_path

    def remove_old_image(self, file_path: str):
        file_path = Path(file_path)
        if file_path.exists() and file_path.is_file():
            os.remove(file_path)
