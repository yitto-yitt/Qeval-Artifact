# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    if hasattr(desired_vector, 'tolist'):
        vector_list = desired_vector.tolist()
    else:
        vector_list = list(desired_vector)
        
    circuit = pq.amplitude_encode(qubits, vector_list)
    
    prog = pq.QProg()
    prog.insert(circuit)
    
    # Measure in reverse order to match Qiskit's little-endian bitstring representation
    for q, c in zip([qubits[2], qubits[1], qubits[0]], cbits):
        prog.insert(pq.Measure(q, c))
        
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
