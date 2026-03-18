import matplotlib.pyplot as plt

def visualize(input, visualizer_id: str):
    if visualizer_id == "prediction-tensor-to-plot":
        return plot_prediction(input)
    else:
        raise ValueError(f"Visualizer {visualizer_id} not found")

def plot_prediction(input):
    for i in range(input.predictions.shape[0]):
        plt.plot(input.predictions[i], color="C%d" % i)
    plt.legend(input.new_object_ids)
    plt.xlim(-0, 150)
    # plt.ylim(0, 0.2)
    plt.xlabel("Tokenized Redshift")
    plt.ylabel("Probability")
    plt.title("AION Redshift Prediction for Photometry+Morphology")
    return plt.gcf()