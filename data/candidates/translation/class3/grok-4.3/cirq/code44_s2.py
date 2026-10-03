# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.CRy(rads=0.2).on(qubits[0], qubits[1]),
        cirq.X.on(qubits[2])
    )
    return circuit
