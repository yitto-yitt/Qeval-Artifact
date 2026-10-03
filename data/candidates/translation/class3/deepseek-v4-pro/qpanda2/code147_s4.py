# EVAL_META: task_id=147, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def mcy(qc):
    gate = Y(qubits[4])
    for ctrl in [qubits[0], qubits[1], qubits[2], qubits[3]]:
        gate = gate.control(ctrl)
    qc.insert(gate)
    return qc

if __name__ == "__main__":
    machine.finalize()
