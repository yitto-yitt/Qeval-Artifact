# EVAL_META: task_id=27, framework=cirq, class=3
import cirq


def apply_op_back():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CX(qubits[0], qubits[1]),
    )
    dag = cirq.CircuitDag.from_circuit(circuit)
    dag.append(cirq.H(qubits[0]))
    return dag
