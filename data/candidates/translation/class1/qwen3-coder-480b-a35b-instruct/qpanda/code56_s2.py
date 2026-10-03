# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            prog << X(qubits[i])
    
    prog << pq.Measure.all(qubits, cbits)
    
    result = machine.run(prog)
    machine.finalize()
    
    counts = {}
    for res in result:
        bitstring = ""
        for i in range(8):
            bitstring += str(res['c' + str(i)])
        if bitstring in counts:
            counts[bitstring] += 1
        else:
            counts[bitstring] = 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
