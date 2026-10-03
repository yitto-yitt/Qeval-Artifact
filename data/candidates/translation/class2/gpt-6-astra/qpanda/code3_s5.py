# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QProg, H, CNOT, measure, CPUQVM


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

        diagram = str(ghz)
        lines = diagram.splitlines()
        width = max((len(line) for line in lines), default=40)
        figure, axis = plt.subplots(
            figsize=(max(6, width * 0.09), max(2, len(lines) * 0.22))
        )
        axis.axis("off")
        axis.text(
            0.02, 0.98, diagram,
            family="monospace",
            ha="left",
            va="top",
            transform=axis.transAxes,
        )
        figure.tight_layout()
        return ghz, figure

    return ghz
