# EVAL_META: task_id=27, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def apply_op_back():
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    
    # In pyQPanda, we don't have direct DAG representation like Qiskit
    # We'll create a new program with the original operations plus the additional H gate
    new_prog = pq.QProg()
    new_prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.H(q[0])
    
    return new_prog

machine.finalize()
