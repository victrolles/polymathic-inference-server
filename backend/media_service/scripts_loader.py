import os
from typing import Optional

from .config.manager import ConfigManager
from .config.structs import VisualizerConfig, PreprocessorConfig, PostprocessorConfig, DatasetFormatterConfig
from shared.structs import ScriptFunction
from shared.utils.functions import load_module

class ScriptsLoader:
    def __init__(self, model_path: str, config_manager: ConfigManager):
        self.config_manager = config_manager

        self.visualizers: list[ScriptFunction] = []
        self.preprocessors: list[ScriptFunction] = []
        self.postprocessors: list[ScriptFunction] = []
        self.dataset_formatters: list[ScriptFunction] = []

        self.visualizers_by_id: dict[str, ScriptFunction] = {}
        self.preprocessors_by_id: dict[str, ScriptFunction] = {}
        self.postprocessors_by_id: dict[str, ScriptFunction] = {}
        self.dataset_formatters_by_id: dict[str, ScriptFunction] = {}

        self._load_scripts(model_path)

    def _load_script_functions(self, src_path: str, file_name: str, script_configs: Optional[list[VisualizerConfig | PreprocessorConfig | PostprocessorConfig | DatasetFormatterConfig]], script_functions: list[ScriptFunction], script_functions_by_id: dict[str, ScriptFunction]) -> None:
        if script_configs is None:
            return
        file_name_extended = f"{file_name}.py"
        full_path = os.path.join(src_path, file_name_extended)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"{file_name_extended} file not found: {full_path}")
        module = load_module(src_path, file_name, file_name_extended)
        for script_config in script_configs:
            callable = getattr(module, script_config.function_name, None)
            if callable is None:
                raise AttributeError(f"Module {full_path} has no '{script_config.function_name}' function")
            script_function = ScriptFunction(config=script_config, callable=callable)
            script_functions.append(script_function)
            script_functions_by_id[script_config.id] = script_function

    def _load_scripts(self, model_path: str) -> None:
        src_path = os.path.join(model_path, "src")
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Scripts not found: {src_path}")

        self._load_script_functions(src_path, "visualizer", self.config_manager.config.visualizers, self.visualizers, self.visualizers_by_id)
        self._load_script_functions(src_path, "preprocessor", self.config_manager.config.preprocessors, self.preprocessors, self.preprocessors_by_id)
        self._load_script_functions(src_path, "postprocessor", self.config_manager.config.postprocessors, self.postprocessors, self.postprocessors_by_id)
        self._load_script_functions(src_path, "dataset_formatter", self.config_manager.config.dataset_formatters, self.dataset_formatters, self.dataset_formatters_by_id)