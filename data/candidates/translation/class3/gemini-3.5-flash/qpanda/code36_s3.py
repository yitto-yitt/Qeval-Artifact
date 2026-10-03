# EVAL_META: task_id=36, framework=qpanda, class=3
import pyqpanda3.core as pq

def bv_function(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAllocMany(n + 1)
    
    prog = pq.QProg()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(qubits[index], qubits[n])
            
    prog._machine = machine
    prog._qubits = qubits
    return prog
