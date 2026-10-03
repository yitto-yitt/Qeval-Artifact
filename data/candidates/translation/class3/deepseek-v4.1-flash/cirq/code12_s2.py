# EVAL_META: task_id=12, framework=cirq, class=3
import cirq

def get_unitary():
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1))
    return cirq.unitary(circuit, qubit_order=[q1, q0])
