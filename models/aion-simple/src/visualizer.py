import matplotlib.pyplot as plt

def prediction_tensor_to_plot(input, modality_id: str):
    if modality_id == "plot":
        return plot_prediction(input)
    else:
        raise ValueError(f"Visualizer {modality_id} not found")

def plot_prediction(input):
    fig, ax = plt.subplots()
    for i in range(input['predictions'].shape[0]):
        ax.plot(input['predictions'][i], color="C%d" % i)
    ax.legend(input['object_ids'])
    ax.set_xlim(-0, 150)
    # ax.set_ylim(0, 0.2)
    ax.set_xlabel("Tokenized Redshift")
    ax.set_ylabel("Probability")
    ax.set_title("AION Redshift Prediction for Photometry+Morphology")
    return fig