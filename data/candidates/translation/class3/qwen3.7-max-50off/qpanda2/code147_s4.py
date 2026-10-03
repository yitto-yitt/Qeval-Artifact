# EVAL_META: task_id=147, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    y_gate = pq.Y(qubits[4])
    ctrl_qubits = [qubits[0], qubits[1], qubits[2], qubits[3]]
    mcy_gate = y_gate.control(ctrl_qubits)
    qc << mcy_gate
    return qc

machine.finalize()
