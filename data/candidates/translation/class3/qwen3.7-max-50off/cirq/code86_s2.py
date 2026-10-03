# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

class LinearFunction(cirq.Gate):
    def __init__(self, num_qubits, max_block_width=None):
        self._num_qubits = num_qubits
        self.max_block_width = max_block_width
        
    def _num_qubits_(self):
        return self._num_qubits

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    
    full_block = cirq.Circuit(
        cirq.H(qubits[0]),
        LinearFunction(5, max_block_width=None)(qubits[0], qubits[1], qubits[2], qubits[3], qubits[4])
    )
    
    limited_block = cirq.Circuit(
        cirq.H(qubits[0]),
        LinearFunction(3, max_block_width=3)(qubits[0], qubits[1], qubits[2]),
        LinearFunction(3, max_block_width=3)(qubits[2], qubits[3], qubits[4])
    )
    
    return full_block, limited_block
