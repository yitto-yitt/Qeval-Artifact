# EVAL_META: task_id=65, framework=pennylane, class=3
import pennylane as qml
from numpy import pi

def QFT(n):
    with qml.tape.QuantumTape() as circuit:
        def swap_registers(circuit, n):
            for qubit in range(n//2):
                qml.SWAP(wires=[qubit, n-qubit-1])
            return circuit
        def qft_rotations(circuit, n):
            """Performs qft on the first n qubits in circuit (without swaps)"""
            if n == 0:
                return circuit
            n -= 1
            qml.Hadamard(wires=n)
            for qubit in range(n):
                qml.ControlledPhaseShift(pi/2**(n-qubit), wires=[qubit, n])
            qft_rotations(circuit, n)
    
        qft_rotations(circuit, n)
        swap_registers(circuit, n)
    return circuit
