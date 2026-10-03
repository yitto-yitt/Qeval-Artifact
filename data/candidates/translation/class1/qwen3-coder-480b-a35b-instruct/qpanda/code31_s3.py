# EVAL_META: task_id=31, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
from typing import Dict

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << pq.Measure.all(qubits, cbits)
    
    result = machine.run_with_configuration(prog, cbits, shots=1000, seed=42)
    
    # Convert result to probability distribution
    total_shots = sum(result.values())
    prob_dist = {key: value / total_shots for key, value in result.items()}
    
    machine.finalize()
    
    return prob_dist
