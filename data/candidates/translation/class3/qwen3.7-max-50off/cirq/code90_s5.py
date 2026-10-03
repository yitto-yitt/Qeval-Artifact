# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    class CustomGate(cirq.Gate):
        def _num_qubits_(self):
            return 2
        
        def _decompose_(self, qubits):
            yield cirq.X(qubits[0])
            yield cirq.H(qubits[1])
            
        def _unitary_(self):
            X = np.array([[0, 1], [1, 0]], dtype=complex)
            H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
            return np.kron(X, H)
            
    q = cirq.LineQubit.range(4)
    custom = CustomGate()
    controlled_custom = custom.controlled(2)
    
    circuit = cirq.Circuit()
    circuit.append(controlled_custom(q[0], q[3], q[1], q[2]))
    return circuit
