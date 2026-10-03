# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import math

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    
    result = machine.run_with_configuration(prog, cbits, 1000)
    
    # Calculate total shots
    import builtins
    total = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {key: value / total for key, value in result.items()}
    
    machine.finalize()
    return prob_dist
