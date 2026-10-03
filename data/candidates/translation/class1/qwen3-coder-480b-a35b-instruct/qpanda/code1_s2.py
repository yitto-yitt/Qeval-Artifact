# EVAL_META: task_id=1, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *

def run_bell_state_simulator():
    machine = CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    
    result = machine.run_with_configuration(prog, cbits, 1000)
    
    # Convert to probability distribution
    total_shots = sum(result.values())
    prob_dist = {key: value / total_shots for key, value in result.items()}
    
    machine.finalize()
    return prob_dist
