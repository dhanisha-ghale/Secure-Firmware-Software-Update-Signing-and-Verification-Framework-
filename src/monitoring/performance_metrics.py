import matplotlib.pyplot as plt
import os

class PerformanceMetrics:
    @staticmethod
    def plot_bargraph(activity_dict, output_path="logs/performance/runtime_analysis.png"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.barh(list(activity_dict.keys()), list(activity_dict.values()), color="skyblue")
        plt.xlabel("Time (seconds)")
        plt.title("Firmware Update Activity Durations")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()