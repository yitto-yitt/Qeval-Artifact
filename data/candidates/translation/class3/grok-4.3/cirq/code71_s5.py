# EVAL_META: task_id=71, framework=cirq, class=3
import cirq

def create_quantum_circuit_based_h0_csx01_h1():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.SX(qubits[1]).controlled_by(qubits[0]),
        cirq.H(qubits[1])
    )
    return circuit
