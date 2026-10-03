# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9, shots=None)
    
    @qml.qnode(dev)
    def circuit():
        # Initialize registers: 3 for a, 3 for b, 3 for ancillary
        a_bits = [int(bit) for bit in format(a, '03b')]
        b_bits = [int(bit) for bit in format(b, '03b')]
        
        # Apply X gates to flip bits that should be 0 (since we start in |0>)
        for i in range(3):
            if a_bits[2-i] == 0:
                qml.PauliX(wires=i)
            if b_bits[2-i] == 0:
                qml.PauliX(wires=i+3)
        
        # Apply CCNOT (Toffoli) gates for AND operation between corresponding bits
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])  # a_i, b_i -> ancillary_i
        
        # Flip all ancillary qubits to get OR instead of NAND
        for i in range(3):
            qml.PauliX(wires=i+6)
        
        # Measure the ancillary qubits
        return qml.sample(wires=[6, 7, 8])
    
    # Run the circuit multiple times to get statistics
    samples = circuit()
    
    # Process samples to get counts
    if len(samples.shape) == 1:
        # Single sample case
        sample_str = ''.join(map(str, samples))
        counts = {sample_str: 1}
    else:
        # Multiple samples case
        count_dict = {}
        for sample in samples:
            sample_str = ''.join(map(str, sample))
            count_dict[sample_str] = count_dict.get(sample_str, 0) + 1
        counts = count_dict
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
