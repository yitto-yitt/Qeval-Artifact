# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, H, X, Z, CNOT, BARRIER, measure

def send_bits(bitstring):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    sender = qubits[0]
    receiver = qubits[1]
    prog = QProg()
    prog << H(sender)
    prog << CNOT(sender, receiver)
    prog << BARRIER()
    if bitstring[1] == "1":
        prog << Z(sender)
    if bitstring[0] == "1":
        prog << X(sender)
    prog << BARRIER()
    prog << CNOT(sender, receiver)
    prog << H(sender)
    prog << measure(sender, cbits[0])
    prog << measure(receiver, cbits[1])
    return prog
