# EVAL_META: task_id=3, framework=cirq, class=2
import cirq
import matplotlib.pyplot as plt


def create_ghz(drawing=False):
    qubits = cirq.LineQubit.range(3)
    ghz = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[0], qubits[2]),
        cirq.measure(*qubits, key="m"),
    )
    if drawing:
        diagram = ghz.to_text_diagram()
        lines = diagram.splitlines()
        figure, ax = plt.subplots(
            figsize=(max(6, max(map(len, lines)) * 0.12), max(2, len(lines) * 0.3))
        )
        ax.text(
            0.5, 0.5, diagram,
            ha="center", va="center", family="monospace", fontsize=12,
        )
        ax.set_axis_off()
        figure.tight_layout()
        return ghz, figure
    return ghz
