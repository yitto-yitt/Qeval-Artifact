# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    q = cirq.LineQubit.range(3)

    circuit = cirq.Circuit([
        cirq.Moment(cirq.H(q[0])),
        cirq.Moment(cirq.CNOT(q[0], q[1])),
        cirq.Moment(cirq.CNOT(q[0], q[2])),
        cirq.Moment(cirq.measure(q[0]), cirq.measure(q[1]), cirq.measure(q[2])),
    ])

    if drawing:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.axis('off')
        ax.text(0.5, 0.5, str(circuit), ha='center', va='center', family='monospace')
        return circuit, fig

    return circuit
