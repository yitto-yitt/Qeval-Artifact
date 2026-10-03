# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def qft_rotations(n_val):
        if n_val == 0:
            return
        n_val -= 1
        circuit.append(cirq.H(qubits[n_val]))
        for qubit in range(n_val):
            exponent = 1.0 / (2 ** (n_val - qubit))
            circuit.append(cirq.CZPowGate(exponent=exponent).on(qubits[qubit], qubits[n_val]))
        qft_rotations(n_val)
        
    def swap_registers():
        for qubit in range(n // 2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))
            
    qft_rotations(n)
    swap_registers()
    return circuit
