# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def QFT(n):
    def swap_registers(wires, n):
        for qubit in range(n//2):
            qml.SWAP(wires=[qubit, n-qubit-1])
    
    def qft_rotations(wires, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return
        n -= 1
        qml.Hadamard(wires=n)
        for qubit in range(n):
            angle = np.pi / 2**(n-qubit)
            qml.ControlledPhaseShift(angle, wires=[qubit, n])
        qft_rotations(wires, n)
    
    dev = qml.device('default.qubit', wires=n)
    
    @qml.qnode(dev)
    def circuit():
        qft_rotations(list(range(n)), n)
        swap_registers(list(range(n)), n)
        return qml.state()
    
    # Create the operation sequence
    ops = []
    
    def qft_rotations_ops(ops_list, n_total, start_idx=0):
        """Builds the operations for QFT rotations"""
        if n_total == 0:
            return
        n = n_total - 1
        ops_list.append(qml.Hadamard(wires=start_idx + n))
        for qubit in range(n):
            angle = np.pi / 2**(n-qubit)
            ops_list.append(qml.ControlledPhaseShift(angle, wires=[start_idx + qubit, start_idx + n]))
        qft_rotations_ops(ops_list, n, start_idx)
    
    def swap_registers_ops(ops_list, n_total, start_idx=0):
        """Builds the operations for swapping registers"""
        for qubit in range(n_total//2):
            ops_list.append(qml.SWAP(wires=[start_idx + qubit, start_idx + n_total - qubit - 1]))
    
    qft_rotations_ops(ops, n)
    swap_registers_ops(ops, n)
    
    return ops
