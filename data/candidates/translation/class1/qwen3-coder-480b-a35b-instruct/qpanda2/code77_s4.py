# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq


def circuit_from_probability_dist(probability_dist):
    max_key = max(probability_dist.keys()) if probability_dist else 0
    num_qubits = math.ceil(math.log2(max_key + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))

    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    # Create the circuit
    prog = pq.QProg()
    
    # Prepare the state using amplitude encoding
    init_state = pq.init_state(amplitudes, qubits)
    prog.insert(init_state)
    
    machine.finalize()
    return prog
