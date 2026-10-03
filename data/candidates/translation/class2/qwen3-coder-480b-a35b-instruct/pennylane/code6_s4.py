# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml


def create_state_prep(num_qubits):
    dev = qml.device('default.qubit', wires=num_qubits)
    
    @qml.qnode(dev)
    def circuit():
        # Prepare the |1> state on all qubits (binary representation of 1)
        qml.BasisState([1] * num_qubits, wires=range(num_qubits))
        return qml.state()
    
    # We need to return the operation that prepares the state, not execute the circuit
    def prep_circuit():
        qml.BasisState([1] * num_qubits, wires=range(num_qubits))
    
    return prep_circuit
