# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import *

def sampler_qiskit():
    # Initialize quantum machine with CPU simulator
    init_global_quantum_machine(QMachineType.CPU)
    # Set the random seed to 42, equivalent to Aer simulator seed
    set_random_seed(42)
    # Allocate two qubits
    q = qAlloc_many(2)
    # Build the Bell circuit: H on q0, CNOT control=q0 target=q1
    prog = QProg() << H(q[0]) << CNOT(q[0], q[1])
    # Run 1024 shots and measure both qubits
    shots = 1024
    results = quick_measure(prog, [q[0], q[1]], shots)
    # Count occurrences
    counts = {}
    for bitstring in results:
        counts[bitstring] = counts.get(bitstring, 0) + 1
    total = sum(counts.values())
    # Normalize to probabilities
    prob_dict = {k: v / total for k, v in counts.items()}
    # Clean up
    finalize_global_quantum_machine()
    return prob_dict
