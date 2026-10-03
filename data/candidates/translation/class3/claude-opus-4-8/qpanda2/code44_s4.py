# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    prog = QCircuit()
    prog << X(qubits[0])
    prog << RY(qubits[2], 0.2).control(qubits[1])
    return prog

if __name__ == "__main__":
    circ = tensor_circuits()
    print(circ)
    machine.finalize()
