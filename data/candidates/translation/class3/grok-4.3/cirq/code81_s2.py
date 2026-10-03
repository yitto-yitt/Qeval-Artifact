# EVAL_META: task_id=81, framework=cirq, class=3
import cirq

def convert_qasm_string_to_quantum_circuit():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1])
    )
    return circuit
