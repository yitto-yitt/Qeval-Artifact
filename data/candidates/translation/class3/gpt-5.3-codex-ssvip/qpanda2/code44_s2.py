# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(3)

def tensor_circuits():
    top = pq.QCircuit()
    top << pq.X(_q[2])

    bottom = pq.QCircuit()
    bottom << pq.CRY(_q[0], _q[1], 0.2)

    tensored = pq.QCircuit()
    tensored << bottom << top

    prog = pq.QProg()
    prog << tensored
    machine.directly_run(prog)
    return tensored

machine.finalize()
