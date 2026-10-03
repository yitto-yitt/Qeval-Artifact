# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit([
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[0], qubits[2]),
        cirq.measure(*qubits, key='result')
    ])
    if drawing:
        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.text(0.01, 0.99, str(circuit), va='top', ha='left', family='monospace')
            ax.axis('off')
            return circuit, fig
        except ImportError:
            return circuit, str(circuit)
    return circuit
