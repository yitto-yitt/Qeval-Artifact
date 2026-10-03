# EVAL_META: task_id=27, framework=cirq, class=3
import cirq


def apply_op_back():
    q0, q1, q2 = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CX(q0, q1),
    )
    dag = cirq.CircuitDag.from_circuit(circuit)
    dag.append(cirq.H(q0))
    return dag
