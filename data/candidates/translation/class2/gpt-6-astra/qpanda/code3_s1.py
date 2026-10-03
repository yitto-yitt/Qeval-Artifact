# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure


def create_ghz(drawing=False):
    ghz = QProg()
    ghz << H(0) << CNOT(0, 1) << CNOT(0, 2)
    for qubit in range(3):
        ghz << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(ghz, 1)

    if drawing:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle

        figure, axes = plt.subplots(figsize=(7, 3))
        for qubit in range(3):
            y = -qubit
            axes.plot([0, 4.5], [y, y], color="black")
            axes.text(-0.15, y, f"q{qubit}", ha="right", va="center")
            axes.add_patch(
                Rectangle(
                    (3.6, y - 0.2), 0.6, 0.4,
                    facecolor="white", edgecolor="black", zorder=3
                )
            )
            axes.text(3.9, y, "M", ha="center", va="center", zorder=4)
            axes.text(4.55, y, f"c{qubit}", ha="left", va="center")

        axes.text(
            0.7, 0, "H", ha="center", va="center",
            bbox=dict(boxstyle="square,pad=0.4", fc="white", ec="black"),
            zorder=4
        )
        for x, target in ((1.7, 1), (2.7, 2)):
            axes.plot([x, x], [0, -target], color="black")
            axes.plot(x, 0, "ko", markersize=6)
            axes.plot(
                x, -target, "o", markersize=15,
                markerfacecolor="white", markeredgecolor="black", zorder=3
            )
            axes.plot(x, -target, "+", color="black", markersize=15, zorder=4)

        axes.set_xlim(-0.5, 5)
        axes.set_ylim(-2.5, 0.5)
        axes.axis("off")
        figure.tight_layout()
        return ghz, figure

    return ghz
