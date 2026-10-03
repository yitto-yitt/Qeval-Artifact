# EVAL_META: task_id=106, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
atexit.register(machine.finalize)


def compose_cnot_dihedral():
    circ1 = pq.QCircuit()
    circ1 << pq.CNOT(q[0], q[1]) << pq.T(q[0])

    circ2 = pq.QCircuit()
    circ2 << pq.CNOT(q[0], q[1]) << pq.T(q[0]) << pq.X(q[1])

    composed_elem = pq.QProg()
    composed_elem << circ1 << circ2
    return composed_elem
