# EVAL_META: task_id=8, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def rx_gate(value=None):
    prog = pq.QProg()
    if value is not None:
        prog << pq.RX(qubits[0], float(value))
    else:
        theta = pq.var("theta")
        prog << pq.RX(qubits[0], theta)
    return prog

machine.finalize()
