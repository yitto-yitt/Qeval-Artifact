# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
import numpy as np

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def swap_registers(circuit, qubits):
        for i in range(len(qubits)//2):
            circuit.append(cirq.SWAP(qubits[i], qubits[len(qubits)-i-1]))
        return circuit
    
    def qft_rotations(circuit, qubits):
        """Performs qft on the qubits in circuit (without swaps)"""
        if len(qubits) == 0:
            return circuit
        qubit = qubits[-1]
        remaining_qubits = qubits[:-1]
        
        circuit.append(cirq.H(qubit))
        
        for i, control_qubit in enumerate(remaining_qubits):
            angle = np.pi / 2**(len(remaining_qubits)-i)
            circuit.append(cirq.CZPowGate(exponent=angle/np.pi)(control_qubit, qubit))
        
        qft_rotations(circuit, remaining_qubits)
    
    qft_rotations(circuit, qubits)
    swap_registers(circuit, qubits)
    return circuit
