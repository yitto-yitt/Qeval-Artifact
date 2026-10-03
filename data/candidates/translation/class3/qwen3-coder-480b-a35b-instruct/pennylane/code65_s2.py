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
                qml.CRot(0, 0, pi/2**(n-qubit), wires=[qubit, n])
            qft_rotations(wires, n)
        
        qft_rotations(list(range(n)), n)
        swap_registers(list(range(n)), n)
        
        # Return the device to access the circuit operations
        return qml.expval(qml.PauliZ(0))
    
    # Execute the circuit to build it
    circuit()
    
    # Return the tape containing the operations
    tape = circuit.qtape
    return tape
