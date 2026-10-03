# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q0))
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.CNOT(q0, q2))
    circuit.append(cirq.measure(q0, q1, q2, key='m'))

    if drawing:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 2))
        ax.axis('off')
        ax.text(0.1, 0.5, circuit.to_text_diagram(), family='monospace', fontsize=10)
        return circuit, fig

    return circuit
