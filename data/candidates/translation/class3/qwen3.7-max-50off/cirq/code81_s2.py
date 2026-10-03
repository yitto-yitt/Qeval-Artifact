# EVAL_META: task_id=81, framework=cirq, class=3
import cirq

def convert_qasm_string_to_quantum_circuit():
    q = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1])
    )
    return circuit
