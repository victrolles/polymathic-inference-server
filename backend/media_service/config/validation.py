from .registry import ConfigRegistry

class ConfigValidationError(Exception):
    pass


def validate_references(registry: ConfigRegistry) -> None:
    data_type_ids = set(registry.data_types_by_id.keys())
    modality_ids = set(registry.modalities_by_id.keys())

    for dataset in registry.config.datasets:
        if dataset.data_type_id not in data_type_ids:
            raise ConfigValidationError(
                f"Dataset '{dataset.id}' references unknown data_type_id '{dataset.data_type_id}'"
            )

    for modality in registry.config.modalities:
        if modality.data_type_id not in data_type_ids:
            raise ConfigValidationError(
                f"Modality '{modality.id}' references unknown data_type_id '{modality.data_type_id}'"
            )

    for dt in registry.config.data_types:
        for field in dt.fields:
            if field.data_type_id not in data_type_ids:
                raise ConfigValidationError(
                    f"Data type '{dt.id}' field '{field.id}' references unknown data_type_id '{field.data_type_id}'"
                )

    for visualizer in registry.config.visualizers:
        if visualizer.input.data_type_id not in data_type_ids:
            raise ConfigValidationError(
                f"Visualizer '{visualizer.id}' input references unknown data_type_id '{visualizer.input.data_type_id}'"
            )
        if visualizer.output.data_type_id not in data_type_ids:
            raise ConfigValidationError(
                f"Visualizer '{visualizer.id}' output references unknown data_type_id '{visualizer.output.data_type_id}'"
            )

    for task in registry.config.tasks:
        if task.data_samples.modality_id and task.data_samples.modality_id not in modality_ids:
            raise ConfigValidationError(
                f"Task '{task.id}' data_samples references unknown modality_id '{task.data_samples.modality_id}'"
            )

        if (
            task.selected_data_samples.modality_id
            and task.selected_data_samples.modality_id not in modality_ids
        ):
            raise ConfigValidationError(
                f"Task '{task.id}' selected_data_samples references unknown modality_id '{task.selected_data_samples.modality_id}'"
            )

        # When `display_multiple_modalities` is enabled, configs may omit `modality_id`
        # and instead specify modality ids through the multi/switch modalities blocks.
        if task.data_outputs.modality_id and task.data_outputs.modality_id not in modality_ids:
            raise ConfigValidationError(
                f"Task '{task.id}' data_outputs references unknown modality_id '{task.data_outputs.modality_id}'"
            )