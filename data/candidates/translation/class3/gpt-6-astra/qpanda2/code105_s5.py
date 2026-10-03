# EVAL_META: task_id=105, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def initialize_cnot_dihedral():
    try:
        program = pq.QProg()
        program << pq.CNOT(qubits[0], qubits[1])
        program << pq.T(qubits[0])
        return pq.get_unitary(program)
    finally:
        machine.finalize()
