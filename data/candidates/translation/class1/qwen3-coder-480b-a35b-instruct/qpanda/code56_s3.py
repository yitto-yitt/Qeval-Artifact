# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *

def not_gate(a):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(8)
    
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            pq.X(qubits[i])
    
    prog = pq.QProg()
    for qubit in qubits:
        prog.insert(pq.Measure(qubit, pq.CBit()))
    
    result = machine.run(prog)
    counts = result.getCounts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
