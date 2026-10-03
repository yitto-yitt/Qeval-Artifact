# EVAL_META: task_id=69, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = pq.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.S(q[1]).control([q[0]])
    prog << pq.H(q[1])
    prog << pq.Sdg(q[0]).control([q[1]])
    return prog
