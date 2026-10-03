# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, H, CNOT, measure, CPUQVM


def create_ghz(drawing=False):
    ghz = QProg()
    ghz << H(0) << CNOT(0, 1) << CNOT(0, 2)
    for qubit in range(3):
        ghz << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(ghz, 1)

    if drawing:
        import matplotlib.pyplot as plt

        figure, axes = plt.subplots(figsize=(8, 3))
        for qubit in range(3):
            y = -qubit
            axes.plot([0, 5], [y, y], color="black")
            axes.text(-0.2, y, f"q{qubit}", ha="right", va="center")
            axes.text(
                4, y, f"M → c{qubit}",
                ha="center", va="center",
                bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="black"),
            )

        axes.text(
            1, 0, "H", ha="center", va="center",
            bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="black"),
        )
        for x, target in ((2, 1), (3, 2)):
            axes.plot([x, x], [0, -target], color="black")
            axes.plot(x, 0, "ko")
            axes.plot(
                x, -target, marker="o", markersize=15,
                markerfacecolor="white", markeredgecolor="black",
            )
            axes.plot(x, -target, marker="+", color="black", markersize=15)

        axes.set_xlim(-0.6, 5.2)
        axes.set_ylim(-2.5, 0.5)
        axes.axis("off")
        figure.tight_layout()
        return ghz, figure

    return ghz
