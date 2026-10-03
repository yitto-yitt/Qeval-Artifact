# EVAL_META: task_id=3, framework=cirq, class=2
import cirq
import matplotlib.pyplot as plt


def create_ghz(drawing=False):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[0], qubits[2]),
        cirq.measure(*qubits, key="result")
    )
    if drawing:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.01, 0.5, circuit.to_text_diagram(), fontsize=10, family="monospace", verticalalignment="center")
        ax.axis("off")
        plt.tight_layout()
        return circuit, fig
    return circuit
