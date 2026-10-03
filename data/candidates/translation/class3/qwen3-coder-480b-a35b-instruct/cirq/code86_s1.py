# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
from cirq.contrib.linear_combinations import LinearCombinationOfGates
from cirq.transformers import collect_linear_combinations

def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4])
    )
    
    # Full block collection (no width limit)
    full_block_circuit = collect_linear_combinations(circuit)
    
    # Limited block collection (max width 3)
    limited_block_circuit = collect_linear_combinations(circuit, max_block_width=3)
    
    return full_block_circuit, limited_block_circuit
