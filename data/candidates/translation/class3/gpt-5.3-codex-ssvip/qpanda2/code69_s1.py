# EVAL_META: task_id=69, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.S(q[1]).control([q[0]])
    prog << pq.H(q[1])
    prog << pq.S(q[0]).dagger().control([q[1]])
    machine.directly_run(prog)
    return prog

machine.finalize()
