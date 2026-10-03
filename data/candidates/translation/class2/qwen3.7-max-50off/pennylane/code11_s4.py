# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml

def get_statevector(circuit):
    dev = qml.device("default.qubit", wires=circuit.num_qubits)
    
    @qml.qnode(dev)
    def qnode():
        qml.from_qiskit(circuit)()
        return qml.state()
        
    return qnode()
