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
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.axis("off")
        ax.text(0.01, 0.5, circuit.to_text_diagram(), fontsize=10, family="monospace", verticalalignment="center", transform=ax.transAxes)
        return circuit, fig
    return circuit
