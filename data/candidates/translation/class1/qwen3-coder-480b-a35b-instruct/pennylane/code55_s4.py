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
        
        # Apply X gates to set initial states (flip 0s to match original logic)
        for i in range(3):
            if a_bits[2-i] == 0:
                qml.PauliX(wires=i)
            if b_bits[2-i] == 0:
                qml.PauliX(wires=i+3)
        
        # Apply CCNOT (Toffoli) gates for AND operation between a and b -> ancillary
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])
        
        # Flip ancillary bits (complement of AND gives OR via De Morgan's law)
        for i in range(3):
            qml.PauliX(wires=i+6)
        
        # Measure the ancillary register
        return qml.sample(wires=[6, 7, 8])
    
    # Sample many times to get statistics
    samples = circuit()
    
    # Process samples to get counts
    if len(samples.shape) == 1:
        # Single sample case
        sample_str = "".join(str(int(b)) for b in samples)
        counts = {sample_str: 1}
    else:
        # Multiple samples case
        count_dict = {}
        for sample in samples:
            sample_str = "".join(str(int(b)) for b in sample)
            count_dict[sample_str] = count_dict.get(sample_str, 0) + 1
        counts = count_dict
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
