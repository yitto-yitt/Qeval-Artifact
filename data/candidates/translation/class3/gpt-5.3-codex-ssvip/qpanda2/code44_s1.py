# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(3)

def tensor_circuits():
    q_top = _global_qubits[0]
    q_bottom_0 = _global_qubits[1]
    q_bottom_1 = _global_qubits[2]

    top_prog = pq.QProg()
    top_prog << pq.X(q_top)

    bottom_prog = pq.QProg()
    bottom_prog << pq.CRY(q_bottom_0, q_bottom_1, 0.2)

    tensored = pq.QProg()
    tensored << bottom_prog << top_prog
    machine.directly_run(tensored)
    return tensored

machine.finalize()
