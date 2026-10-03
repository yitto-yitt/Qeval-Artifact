# EVAL_META: task_id=65, framework=cirq, class=3
import cirq

def QFT(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    
    def qft_rotations(n_qubits):
        if n_qubits == 0:
            return
        n_qubits -= 1
        target = qubits[n_qubits]
        circuit.append(cirq.H(target))
        for i in range(n_qubits):
            control = qubits[i]
            exponent = 1 / 2**(n_qubits - i)
            circuit.append(cirq.CZPowGate(exponent=exponent).on(control, target))
        qft_rotations(n_qubits)
        
    qft_rotations(n)
    
    for i in range(n // 2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n - i - 1]))
        
    return circuit
