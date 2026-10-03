# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    # SX gate on q[3], controlled by q[0], q[1], q[2]
    c3sx_gate = pq.SX(q[3]).control([q[0], q[1], q[2]])
    prog.insert(c3sx_gate)
    return prog

# Manual Cleanup
machine.finalize()
