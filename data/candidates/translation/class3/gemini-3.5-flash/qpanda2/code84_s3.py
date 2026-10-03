# EVAL_META: task_id=84, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    prog = pq.QProg()
    u3_gate = pq.U3(q[1], 0.3, 0.2, 0.1)
    controlled_gate = u3_gate.control([q[0]])
    prog.insert(controlled_gate)
    return prog

machine.finalize()
