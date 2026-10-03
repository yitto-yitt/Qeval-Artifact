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
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    prog.insert(pq.Measure(qubits[1], cbits[1]))
    
    result = machine.run_with_configuration(prog, cbits, shots=1000, seed=42)
    
    # Convert results to probability distribution
    counts = {}
    for outcome, count in result.items():
        # Reverse the bitstring to match Qiskit's convention
        reversed_outcome = outcome[::-1]
        counts[reversed_outcome] = count
    
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    return prob_dist
