# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def qft_rotations(n_q):
        if n_q == 0:
            return
        n_q -= 1
        circuit.append(cirq.H(qubits[n_q]))
        for qubit in range(n_q):
            exponent = 1.0 / (2 ** (n_q - qubit))
            circuit.append(cirq.CZPowGate(exponent=exponent).on(qubits[qubit], qubits[n_q]))
        qft_rotations(n_q)
        
    def swap_registers():
        for qubit in range(n // 2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))
            
    qft_rotations(n)
    swap_registers()
    
    return circuit
