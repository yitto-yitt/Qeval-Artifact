# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    # bottom circuit (2 qubits): CRY(0.2) with control qubit 0 and target qubit 1
    prog.insert(pq.CRY(q[0], q[1], 0.2))
    # top circuit (1 qubit): X gate
    prog.insert(pq.X(q[2]))
    return prog

machine.finalize()
