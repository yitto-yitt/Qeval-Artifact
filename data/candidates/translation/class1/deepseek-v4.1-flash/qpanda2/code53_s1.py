# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def xor_gate(a, b):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog << X(qubits[i])
        if (b >> i) & 1:
            prog << X(qubits[i])
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
    shots = 1024
    result = run_with_configuration(prog, cbits, shots)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
