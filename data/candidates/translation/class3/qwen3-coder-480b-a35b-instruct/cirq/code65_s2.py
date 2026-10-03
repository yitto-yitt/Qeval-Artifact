# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
import numpy as np

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def swap_registers(circuit, qubits):
        num_qubits = len(qubits)
        for i in range(num_qubits // 2):
            circuit.append(cirq.SWAP(qubits[i], qubits[num_qubits - i - 1]))
        return circuit
    
    def qft_rotations(circuit, qubits):
        """Performs qft on the qubits in circuit (without swaps)"""
        if len(qubits) == 0:
            return circuit
        # Work with the last qubit in the list
        if len(qubits) == 1:
            circuit.append(cirq.H(qubits[0]))
            return circuit
        
        last_qubit = qubits[-1]
        remaining_qubits = qubits[:-1]
        
        circuit.append(cirq.H(last_qubit))
        
        for i, qubit in enumerate(remaining_qubits):
            angle = np.pi / (2 ** (len(remaining_qubits) - i))
            circuit.append(cirq.CZPowGate(exponent=angle / np.pi)(qubit, last_qubit))
        
        qft_rotations(circuit, remaining_qubits)
    
    if n > 0:
        qft_rotations(circuit, qubits)
        swap_registers(circuit, qubits)
    
    return circuit
