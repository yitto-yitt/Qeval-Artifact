# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    qc = pq.QCircuit()
    qc << pq.H(qubits[0])
    theta = 0.0
    qc << pq.RZ(qubits[0], theta)
    return qc

machine.finalize()
