from typing import Any
import os

import PIL.Image
import matplotlib.figure

from .config.data_kind import DataKind
from .config.structs import DataTypeConfig

class MediaConverter:
    def __init__(self, media_files_path: str):
        self.media_files_path = media_files_path

    def _get_full_path(self, file_name: str, file_ext: str) -> str:
        file_name_extended = f"{file_name}{file_ext}"
        full_path = os.path.join(self.media_files_path, file_name_extended)
        return full_path

    def _save_image(self, data: Any, file_name: str, data_type_config: DataTypeConfig) -> str:
        file_ext = ".png"
        full_path = self._get_full_path(file_name, file_ext)
        if isinstance(data, PIL.Image.Image):
            data.save(
                full_path,
                format="PNG"
            )
            return full_path
        elif isinstance(data, matplotlib.figure.Figure):
            data.savefig(
                full_path,
                dpi=data_type_config.dpi
            )
            return full_path
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def _save_video(self, data: Any, file_name: str, data_type_config: DataTypeConfig) -> str:
        file_ext = ".gif"
        full_path = self._get_full_path(file_name, file_ext)
        if isinstance(data, matplotlib.animation.Animation):
            data.save(
                full_path,
                writer="pillow",
                fps=data_type_config.fps,
                savefig_kwargs={"pad_inches": 0}
            )
            return full_path
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def save_object(self, data: Any, file_name: str, data_type_config: DataTypeConfig) -> str:
        if data_type_config.kind == DataKind.IMAGE:
            return self._save_image(data, file_name, data_type_config)
        elif data_type_config.kind == DataKind.VIDEO:
            return self._save_video(data, file_name, data_type_config)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")