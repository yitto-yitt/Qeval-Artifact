# EVAL_META: task_id=0, framework=pennylane, class=3
import pennylane as qml

def create_quantum_circuit(n_qubits):
    return qml.tape.QuantumTape([qml.Identity(wires=i) for i in range(n_qubits)])
