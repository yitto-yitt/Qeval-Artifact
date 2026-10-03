# EVAL_META: task_id=65, framework=cirq, class=3
import cirq
import numpy as np

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def qft_rotations(n_val):
        if n_val == 0:
            return
        n_val -= 1
        circuit.append(cirq.H(qubits[n_val]))
        for qubit in range(n_val):
            circuit.append(cirq.ZPowGate(exponent=1/2**(n_val-qubit)).controlled().on(qubits[qubit], qubits[n_val]))
        qft_rotations(n_val)

    def swap_registers(n_val):
        for qubit in range(n_val // 2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n_val - qubit - 1]))

    qft_rotations(n)
    swap_registers(n)
    
    return circuit
