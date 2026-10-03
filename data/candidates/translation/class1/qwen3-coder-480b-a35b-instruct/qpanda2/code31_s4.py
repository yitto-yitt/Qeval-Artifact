# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import math

def sampler_qiskit():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << MeasureAll(qubits, cbits)
    
    # Set random seed
    machine.set_random_engine_seed(42)
    
    result = run_with_configuration(machine, prog, cbits, shots=1000)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    destroy_quantum_machine(machine)
    return prob_dist
