# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    dev = qml.device('default.qubit', wires=n)
    
    @qml.qnode(dev)
    def circuit():
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
                qml.ctrl(qml.RZ, control=qubit, target=n)(pi/2**(n-qubit))
            qft_rotations(wires, n)
        
        qft_rotations(list(range(n)), n)
        swap_registers(list(range(n)), n)
        return qml.state()
    
    # Build the operation sequence manually
    ops = []
    
    def build_qft_ops(n):
        """Builds the QFT operations"""
        def add_qft_rotations(current_n):
            if current_n == 0:
                return
            current_n -= 1
            ops.append(qml.Hadamard(wires=current_n))
            for qubit in range(current_n):
                ops.append(qml.ctrl(qml.RZ, control=qubit, target=current_n)(pi/2**(current_n-qubit)))
            add_qft_rotations(current_n)
        
        add_qft_rotations(n)
        
        # Add swaps
        for qubit in range(n//2):
            ops.append(qml.SWAP(wires=[qubit, n-qubit-1]))
    
    build_qft_ops(n)
    
    # Create a template that applies all operations
    def qft_template(wires):
        for op in ops:
            qml.apply(op)
    
    return qft_template
