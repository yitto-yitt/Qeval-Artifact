# EVAL_META: task_id=84, framework=qpanda, class=3
import pyqpanda3.core as pq

def controlled_custom_unitary_circuit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    u3_gate = pq.U3(q[1], 0.3, 0.2, 0.1)
    controlled_gate = u3_gate.control([q[0]])
    prog.insert(controlled_gate)
    return prog
