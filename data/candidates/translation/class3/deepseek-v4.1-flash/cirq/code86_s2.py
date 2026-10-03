# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
from cirq.transformers import merge_k_qubit_unitaries

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    qc = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CX(qubits[0], qubits[1]),
        cirq.CX(qubits[1], qubits[2]),
        cirq.CX(qubits[2], qubits[3]),
        cirq.CX(qubits[3], qubits[4]),
    )
    
    def is_cx(op):
        return op.gate == cirq.CX
    
    full_block = merge_k_qubit_unitaries(qc, k=5, mergeable=is_cx)
    limited_block = merge_k_qubit_unitaries(qc, k=3, mergeable=is_cx)
    
    return full_block, limited_block
