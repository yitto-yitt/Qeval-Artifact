# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def QFT(n):
    dev = qml.device('default.qubit', wires=n)
    
    @qml.qnode(dev)
    def circuit():
        def swap_registers(wires):
            for qubit in range(wires//2):
                qml.SWAP(wires=[qubit, wires-qubit-1])
        
        def qft_rotations(wires):
            """Performs qft on the first n qubits in circuit (without swaps)"""
            if wires == 0:
                return
            wires -= 1
            qml.Hadamard(wires=wires)
            for qubit in range(wires):
                qml.ctrl(qml.RZ, control=qubit, target=wires)(np.pi/2**(wires-qubit), wires=[qubit, wires])
            qft_rotations(wires)
        
        qft_rotations(n)
        swap_registers(n)
        return qml.state()
    
    # Create the operation sequence without executing
    ops = []
    
    def apply_ops():
        def swap_registers_inner(wires):
            for qubit in range(wires//2):
                ops.append(qml.SWAP(wires=[qubit, wires-qubit-1]))
        
        def qft_rotations_inner(wires):
            """Performs qft on the first n qubits in circuit (without swaps)"""
            if wires == 0:
                return
            wires -= 1
            ops.append(qml.Hadamard(wires=wires))
            for qubit in range(wires):
                ops.append(qml.CRot(0, 0, np.pi/2**(wires-qubit), wires=[qubit, wires]))
            qft_rotations_inner(wires)
        
        qft_rotations_inner(n)
        swap_registers_inner(n)
    
    apply_ops()
    
    # Return a template that applies these operations
    def template(wires):
        for op in ops:
            qml.apply(op)
    
    return template
