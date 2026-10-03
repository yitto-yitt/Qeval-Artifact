# EVAL_META: task_id=52, framework=qpanda2, class=1
import builtins
from pyqpanda import *
def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    if bitstring[1] == "1":
        prog << Z(qubits[0])
    if bitstring[0] == "1":
        prog << X(qubits[0])
    prog << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])
    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    measured = max(counts, key=counts.get)
    return measured
