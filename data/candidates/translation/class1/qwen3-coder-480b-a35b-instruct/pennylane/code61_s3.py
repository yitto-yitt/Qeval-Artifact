# EVAL_META: task_id=61, framework=pennylane, class=1
import pennylane as qml


def create_quantum_circuit_with_one_qubit_and_measure():
    dev = qml.device('default.qubit', wires=1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        return qml.sample(qml.PauliZ(0))
    
    # Create the tape manually to mimic the circuit structure
    with qml.tape.QuantumTape() as tape:
        qml.sample(qml.PauliZ(0))
    
    return tape
