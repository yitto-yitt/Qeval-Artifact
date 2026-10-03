# EVAL_META: task_id=36, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
try:
    machine.set_configure(64, 64)
except Exception:
    pass
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def bv_function(s):
    n = len(s)
    qc = pq.QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.insert(pq.CNOT(qubits[index], qubits[n]))
    return qc

atexit.register(lambda: machine.finalize())
