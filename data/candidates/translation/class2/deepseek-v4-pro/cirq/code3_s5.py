# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CX(q[0], q[1]),
        cirq.CX(q[0], q[2]),
        cirq.measure(*q, key='m')
    )
    if drawing:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.text(0.1, 0.5, str(circuit), family='monospace', fontsize=12)
        return circuit, fig
    return circuit
