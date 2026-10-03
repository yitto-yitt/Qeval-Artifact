# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import *

def bell_each_shot():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    result = qvm.run_with_configuration(prog, cbits, 10)
    total = sum(result.values())
    bitstrings = {}
    for k, v in result.items():
        bs = bin(k)[2:].zfill(2)
        bitstrings[bs] = bitstrings.get(bs, 0) + v
    return {key: value / total for key, value in bitstrings.items()}
