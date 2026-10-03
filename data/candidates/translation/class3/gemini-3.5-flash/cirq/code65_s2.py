# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n: int) -> cirq.Circuit:
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(n)
    
    def swap_registers(circuit, n):
        for qubit in range(n // 2):
            circuit.append(cirq.SWAP(qubits[qubit], qubits[n - qubit - 1]))
            
    def qft_rotations(circuit, n):
        if n == 0:
            return
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for qubit in range(n):
            exponent = 1.0 / (2 ** (n - qubit))
            circuit.append((cirq.CZ ** exponent)(qubits[qubit], qubits[n]))
        qft_rotations(circuit, n)
        
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
