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
        fig, ax = plt.subplots()
        ax.text(0.0, 1.0, ghz.to_text_diagram(), family="monospace", va="top")
        ax.axis("off")
        fig.tight_layout()
        return ghz, fig
    return ghz
