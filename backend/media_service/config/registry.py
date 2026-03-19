from .structs import AppConfig

class ConfigRegistry:
    def __init__(self, config: AppConfig):
        self.config = config

        self.sizes_by_id = {x.id: x for x in config.sizes}
        self.data_types_by_id = {x.id: x for x in config.data_types}
        self.visualizers_by_id = {x.id: x for x in config.visualizers}
        self.datasets_by_id = {x.id: x for x in config.datasets}
        self.modalities_by_id = {x.id: x for x in config.modalities}
        self.tasks_by_id = {x.id: x for x in config.tasks}