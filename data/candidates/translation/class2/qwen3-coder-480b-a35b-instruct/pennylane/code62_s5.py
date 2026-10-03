# EVAL_META: task_id=62, framework=pennylane, class=2
import pennylane as qml


def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    dev = qml.device('default.qubit', wires=num_qubits)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(len(basis)):
            if state[i] == 1:
                qml.PauliX(wires=i)
            if basis[i] == 1:
                qml.Hadamard(wires=i)
        return qml.state()
    
    # Create the tape to get the operations
    tape = circuit.qtape
    ops = tape.operations
    
    # Reconstruct the circuit using templates or direct operations
    def reconstructed_circuit():
        for op in ops:
            qml.apply(op)
        return qml.state()
    
    return reconstructed_circuit
