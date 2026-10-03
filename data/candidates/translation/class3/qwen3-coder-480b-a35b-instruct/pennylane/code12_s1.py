# EVAL_META: task_id=12, framework=pennylane, class=3
import pennylane as qml
import numpy as np


def get_unitary():
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.state()
    
    # Create the unitary by applying the circuit to each computational basis state
    n_wires = 2
    dim = 2 ** n_wires
    unitary = np.zeros((dim, dim), dtype=complex)
    
    for i in range(dim):
        # Prepare the initial state as the computational basis state |i>
        @qml.qnode(dev)
        def prepare_and_run():
            # Convert i to binary representation and prepare that state
            for j in range(n_wires):
                if (i >> j) & 1:
                    qml.PauliX(wires=j)
            
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            return qml.state()
        
        unitary[:, i] = prepare_and_run()
    
    return unitary
