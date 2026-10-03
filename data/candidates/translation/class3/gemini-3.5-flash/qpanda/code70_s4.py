# EVAL_META: task_id=70, framework=qpanda, class=3
import pyqpanda3.core as pq

_machines = []

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    machine = pq.CPUQVM()
    machine.init_qvm()
    _machines.append(machine)
    q = machine.qAlloc_many(3)
    prog = pq.QProg()
    prog << pq.H(q[0]) \
         << pq.CSWAP(q[0], q[1], q[2]) \
         << pq.H(q[1]) \
         << pq.S(q[0]).dagger().control([q[1]])
    return prog
