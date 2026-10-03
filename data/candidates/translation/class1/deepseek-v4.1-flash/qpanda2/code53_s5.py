# EVAL_META: task_id=53, framework=qpanda2, class=1
from pyqpanda import *

def xor_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if ((a >> i) & 1) ^ ((b >> i) & 1):
            prog << X(qubits[i])
    for i in range(8):
        prog << MEASURE(qubits[i], cbits[i])
    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)
    machine.finalize()
    return {key: value / shots for key, value in result.items()}
