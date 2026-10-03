# EVAL_META: task_id=38, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.RZ(qubits[1], theta).control([qubits[0]])
    prog << pq.H(qubits[1])
    prog << pq.RY(qubits[0], theta).control([qubits[1]])
    machine.directly_run(prog)
    return prog


atexit.register(machine.finalize)
