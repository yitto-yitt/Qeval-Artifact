# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def swap_registers(circuit, n):
        for i in range(n // 2):
            circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))
        return circuit

    def qft_rotations(circuit, n):
        if n == 0:
            return circuit
        n -= 1
        circuit.append(cirq.H(qubits[n]))
        for i in range(n):
            circuit.append(cirq.CZPowGate(exponent=1.0 / (2 ** (n - i)))(qubits[i], qubits[n]))
        qft_rotations(circuit, n)
        
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit
