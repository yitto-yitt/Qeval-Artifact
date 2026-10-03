# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CSWAP(q[0], q[1], q[2]))
    prog.insert(pq.H(q[1]))
    prog.insert(pq.Sdag(q[0]).control([q[1]]))
    machine.directly_run(prog)
    return prog

machine.finalize()
