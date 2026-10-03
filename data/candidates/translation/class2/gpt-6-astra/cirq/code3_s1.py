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
        diagram = ghz.to_text_diagram(use_unicode_characters=False)
        lines = diagram.splitlines()
        figure, axis = plt.subplots(
            figsize=(max(6, max(map(len, lines)) * 0.1), max(2, len(lines) * 0.3))
        )
        axis.text(
            0.5, 0.5, diagram,
            family="monospace",
            ha="center",
            va="center",
            transform=axis.transAxes,
        )
        axis.set_axis_off()
        figure.tight_layout()
        return ghz, figure
    return ghz
