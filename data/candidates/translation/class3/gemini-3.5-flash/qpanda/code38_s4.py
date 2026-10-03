# EVAL_META: task_id=38, framework=qpanda, class=3
import pyqpanda3.core as pq

_machine = pq.CPUQVM()
_machine.init_qvm()
_qubits = _machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = pq.QProg()
    prog << pq.H(_qubits[0])
    prog << pq.RZ(_qubits[1], theta).control([_qubits[0]])
    prog << pq.H(_qubits[1])
    prog << pq.RY(_qubits[0], theta).control([_qubits[1]])
    return prog
