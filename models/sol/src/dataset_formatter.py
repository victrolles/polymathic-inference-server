def format_sol_dataset(data: list[dict]) -> list[dict]:
    new_subset = []
    for element in data:
        new_element = {
            "x_obs": element["x_obs"]
        }
        new_subset.append(new_element)
    return new_subset