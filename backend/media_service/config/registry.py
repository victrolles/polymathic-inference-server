from .structs import AppConfig

class ConfigRegistry:
    def __init__(self, config: AppConfig):
        self.config = config

        self.sizes_by_id = {x.id: x for x in config.sizes}
        self.data_types_by_id = {x.id: x for x in config.data_types}
        if config.visualizers is None:
            self.visualizers_by_id = None
        else:
            self.visualizers_by_id = {x.id: x for x in config.visualizers}
        if config.preprocessors is None:
            self.preprocessors_by_id = None
        else:
            self.preprocessors_by_id = {x.id: x for x in config.preprocessors}
        if config.postprocessors is None:
            self.postprocessors_by_id = None
        else:
            self.postprocessors_by_id = {x.id: x for x in config.postprocessors}
        if config.dataset_formatters is None:
            self.dataset_formatters_by_id = None
        else:
            self.dataset_formatters_by_id = {x.id: x for x in config.dataset_formatters}
        self.datasets_by_id = {x.id: x for x in config.datasets}
        self.modalities_by_id = {x.id: x for x in config.modalities}
        self.tasks_by_id = {x.id: x for x in config.tasks}