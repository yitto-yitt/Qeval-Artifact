# EVAL_META: task_id=1, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
from pyqpanda3.algorithms import *
from pyqpanda3.machine import *

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    
    result = machine.run_with_configuration(prog, cbits, 1000)
    
    # Convert to probability distribution
    total_shots = sum(result.values())
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    machine.finalize()
    return prob_dist
