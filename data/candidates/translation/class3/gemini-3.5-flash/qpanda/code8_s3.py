# EVAL_META: task_id=8, framework=qpanda, class=3
import pyqpanda3.core as pq

def rx_gate(value=None):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(1)
    prog = pq.QProg()
    
    theta = value if value is not None else 0.0
    prog << pq.RX(qubits[0], theta)
    return prog
