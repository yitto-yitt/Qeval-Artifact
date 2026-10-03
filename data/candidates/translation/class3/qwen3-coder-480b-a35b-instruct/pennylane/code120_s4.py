# EVAL_META: task_id=120, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_diagonal_circuit(diag):
    diag_array = np.array(diag)
    num_qubits = int(np.log2(len(diag_array)))
    
    def circuit():
        qml.Diagonal(diag_array, wires=range(num_qubits))
    
    dev = qml.device('default.qubit', wires=num_qubits)
    qnode = qml.QNode(circuit, dev)
    qnode()
    
    return qnode.func
