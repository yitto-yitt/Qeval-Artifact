# EVAL_META: task_id=2, framework=qpanda2, class=2
import pyqpanda as pq

def create_bell_statevector():
    machine = pq.CPUQVM()
    machine.initQVM()
    qubits = machine.qAllocMany(2)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.CNOT(qubits[0], qubits[1])
    machine.directlyRun(prog)
    return machine.getQState()
