# EVAL_META: task_id=3, framework=cirq, class=2
import cirq
import matplotlib.pyplot as plt

def create_ghz(drawing=False):
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[0], q[2]),
        cirq.measure(*q, key='m')
    )
    if drawing:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, str(circuit), ha='center', va='center', fontsize=10, family='monospace')
        ax.axis('off')
        return circuit, fig
    return circuit
