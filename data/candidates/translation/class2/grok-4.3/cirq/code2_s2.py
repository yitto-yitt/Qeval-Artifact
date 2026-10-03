# EVAL_META: task_id=2, framework=cirq, class=2
import cirq

def create_bell_statevector():
    qubits = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(cirq.H(qubits[0]), cirq.CNOT(qubits[0], qubits[1]))
    return cirq.final_state_vector(circuit)
