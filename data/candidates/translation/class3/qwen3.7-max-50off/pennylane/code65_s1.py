# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    ops = []
    
    def qft_rotations(n_qubits):
        if n_qubits == 0:
            return
        n_qubits -= 1
        ops.append(qml.Hadamard(wires=n_qubits))
        for qubit in range(n_qubits):
            ops.append(qml.ControlledPhaseShift(pi / 2**(n_qubits - qubit), wires=[qubit, n_qubits]))
        qft_rotations(n_qubits)
        
    def swap_registers(n_qubits):
        for qubit in range(n_qubits // 2):
            ops.append(qml.SWAP(wires=[qubit, n_qubits - qubit - 1]))
            
    qft_rotations(n)
    swap_registers(n)
    return ops
