# EVAL_META: task_id=8, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    q = _global_qubits[0]
    prog = pq.QProg()
    angle = 0.0 if value is None else float(value)
    prog.insert(pq.RX(q, angle))
    return prog

machine.finalize()
