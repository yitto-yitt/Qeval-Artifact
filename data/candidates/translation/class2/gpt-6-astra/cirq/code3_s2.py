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
        fig, ax = plt.subplots(
            figsize=(max(6, max(map(len, lines)) * 0.12), max(2, len(lines) * 0.35))
        )
        ax.text(
            0.5, 0.5, diagram,
            ha="center", va="center",
            family="monospace", fontsize=12,
            transform=ax.transAxes,
        )
        ax.set_axis_off()
        fig.tight_layout()
        return ghz, fig
    return ghz
