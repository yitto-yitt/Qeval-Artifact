# EVAL_META: task_id=3, framework=cirq, class=2
import cirq


def create_ghz(drawing=False):
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.CNOT(q[0], q[2]),
        cirq.measure(*q, key='result'),
    )
    if drawing:
        fig = cirq.vis.plot_circuit(circuit)
        return circuit, fig
    return circuit
