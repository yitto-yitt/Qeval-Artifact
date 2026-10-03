# EVAL_META: task_id=11, framework=pennylane, class=2
import pennylane as qml
from pennylane import numpy as np

def get_statevector(circuit):
    dev = qml.device('default.qubit', wires=circuit.num_qubits)
    
    @qml.qnode(dev)
    def circuit_qnode():
        for instruction in circuit.data:
            gate = instruction[0]
            qubits = [q.index for q in instruction[1]]
            
            if gate.name == 'h':
                qml.Hadamard(wires=qubits[0])
            elif gate.name == 'x':
                qml.PauliX(wires=qubits[0])
            elif gate.name == 'y':
                qml.PauliY(wires=qubits[0])
            elif gate.name == 'z':
                qml.PauliZ(wires=qubits[0])
            elif gate.name == 'rx':
                qml.RX(gate.params[0], wires=qubits[0])
            elif gate.name == 'ry':
                qml.RY(gate.params[0], wires=qubits[0])
            elif gate.name == 'rz':
                qml.RZ(gate.params[0], wires=qubits[0])
            elif gate.name == 'cx':
                qml.CNOT(wires=[qubits[0], qubits[1]])
            elif gate.name == 'cz':
                qml.CZ(wires=[qubits[0], qubits[1]])
            elif gate.name == 'swap':
                qml.SWAP(wires=[qubits[0], qubits[1]])
        
        return qml.state()
    
    return circuit_qnode()
