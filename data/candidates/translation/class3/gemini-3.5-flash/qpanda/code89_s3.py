# EVAL_META: task_id=89, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_controlled_hgate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    prog = pq.QProg()
    controlled_h = pq.H(qubits[2]).control([qubits[0], qubits[1]])
    prog << controlled_h
    return prog
