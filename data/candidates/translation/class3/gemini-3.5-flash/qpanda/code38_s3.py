# EVAL_META: task_id=38, framework=qpanda, class=3
import pyqpanda3.core as pq

_machines = []

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    machine = pq.CPUQVM()
    machine.init_qvm()
    _machines.append(machine)
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) \
         << pq.CRZ(q[0], q[1], theta) \
         << pq.H(q[1]) \
         << pq.CRY(q[1], q[0], theta)
    return prog
