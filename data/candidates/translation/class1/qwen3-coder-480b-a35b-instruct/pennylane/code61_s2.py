# EVAL_META: task_id=61, framework=pennylane, class=1
import pennylane as qml


def create_quantum_circuit_with_one_qubit_and_measure():
    dev = qml.device('default.qubit', wires=1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        return qml.sample(qml.PauliZ(0))
    
    # This creates the quantum circuit with measurement
    # In PennyLane, we define the circuit as a function with measurements
    return circuit
