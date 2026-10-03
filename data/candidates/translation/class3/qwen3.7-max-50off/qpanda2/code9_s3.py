# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_efficientSU2():
    circ = pq.QCircuit()
    for i in range(3):
        circ << pq.RY(q[i], 0.0) << pq.RZ(q[i], 0.0)
    circ << pq.Barrier(q)
    circ << pq.CNOT(q[0], q[1]) << pq.CNOT(q[1], q[2])
    circ << pq.Barrier(q)
    for i in range(3):
        circ << pq.RY(q[i], 0.0) << pq.RZ(q[i], 0.0)
    return circ

machine.finalize()
