# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def QFT(n):
    def swap_registers(ops, n):
        for qubit in range(n//2):
            ops.append(qml.SWAP(wires=[qubit, n-qubit-1]))
        return ops
    
    def qft_rotations(ops, n):
        """Performs qft on the first n qubits in circuit (without swaps)"""
        if n == 0:
            return ops
        n -= 1
        ops.append(qml.Hadamard(wires=n))
        for qubit in range(n):
            ops.append(qml.CRot(0, 0, np.pi/2**(n-qubit), wires=[qubit, n]))
        qft_rotations(ops, n)
    
    ops = []
    qft_rotations(ops, n)
    swap_registers(ops, n)
    
    dev = qml.device('default.qubit', wires=n)
    
    @qml.qnode(dev)
    def circuit():
        for op in ops:
            qml.apply(op)
        return qml.state()
    
    # Create a template that applies the operations
    def qft_template(wires):
        nonlocal ops
        for op in ops:
            qml.apply(op)
    
    # Return the operations list to represent the circuit
    return ops
