# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def visualize_bell_states():
    # Prepare phi_plus circuit
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog_plus = pq.QProg()
    prog_plus.insert(pq.H(qubits[0]))
    prog_plus.insert(pq.CNOT(qubits[0], qubits[1]))
    prog_plus << pq.Measure(qubits[0], cbits[0]) << pq.Measure(qubits[1], cbits[1])
    
    result_plus = machine.run(prog_plus, shots=1000)
    counts_plus = result_plus.get_dict()
    
    # Reset machine for phi_minus
    machine2 = pq.QMachine()
    qubits2 = machine2.qAlloc_many(2)
    cbits2 = machine2.cAlloc_many(2)
    
    prog_minus = pq.QProg()
    prog_minus.insert(pq.X(qubits2[0]))
    prog_minus.insert(pq.H(qubits2[0]))
    prog_minus.insert(pq.CNOT(qubits2[0], qubits2[1]))
    prog_minus << pq.Measure(qubits2[0], cbits2[0]) << pq.Measure(qubits2[1], cbits2[1])
    
    result_minus = machine2.run(prog_minus, shots=1000)
    counts_minus = result_minus.get_dict()
    
    # Calculate probabilities
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    prob_plus = {key: value / total_plus for key, value in counts_plus.items()}
    prob_minus = {key: value / total_minus for key, value in counts_minus.items()}
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
