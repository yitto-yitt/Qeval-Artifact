# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    top = pq.QCircuit()
    top << pq.X(q[2])

    bottom = pq.QCircuit()
    bottom << pq.RY(q[1], 0.2).control(q[0])

    tensored = pq.QCircuit()
    tensored << bottom << top
    return tensored

machine.finalize()
