# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, CPUQVM, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QProg()
    ghz << H(0)
    ghz << CNOT(0, 1)
    ghz << CNOT(0, 2)
    ghz << measure(0, 0)
    ghz << measure(1, 1)
    ghz << measure(2, 2)

    simulator = CPUQVM()
    simulator.run(ghz, 1)

    if drawing:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 3))
        for qubit in range(3):
            y = 2 - qubit
            ax.hlines(y, 0, 5, color="black")
            ax.text(-0.15, y, f"q{qubit}", ha="right", va="center")
            ax.text(
                4, y, "M",
                ha="center", va="center",
                bbox=dict(boxstyle="square,pad=0.35", fc="white", ec="black"),
            )
            ax.text(4.5, y + 0.18, f"c{qubit}", ha="center", fontsize=9)

        ax.text(
            1, 2, "H",
            ha="center", va="center",
            bbox=dict(boxstyle="square,pad=0.35", fc="white", ec="black"),
        )
        for x, target_y in ((2, 1), (3, 0)):
            ax.vlines(x, target_y, 2, color="black")
            ax.plot(x, 2, "ko")
            ax.plot(
                x, target_y, marker="o", markersize=16,
                markerfacecolor="white", markeredgecolor="black",
            )
            ax.plot(x, target_y, marker="+", markersize=16, color="black")

        ax.set_xlim(-0.6, 5.2)
        ax.set_ylim(-0.5, 2.5)
        ax.axis("off")
        fig.tight_layout()
        return ghz, fig

    return ghz
