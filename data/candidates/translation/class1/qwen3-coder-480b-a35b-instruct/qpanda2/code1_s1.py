# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import math

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.Measure(qubits[0], cbits[0]) \
         << pq.Measure(qubits[1], cbits[1])
    
    result = machine.run_with_configuration(prog, cbits, 1000)
    machine.finalize()
    
    total_shots = 1000
    counts = {}
    for key, value in result.items():
        # Convert integer keys to binary string format (e.g., '00', '01', '10', '11')
        binary_str = format(int(key), f'0{len(cbits)}b')
        counts[binary_str] = value
    
    # Normalize counts to probabilities
    probabilities = {key: value / total_shots for key, value in counts.items()}
    
    return probabilities
