# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, H, S

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_quantum_circuit_based_h0_csx01_h1():
    program = QProg()
    program << H(qubits[0])
    program << H(qubits[1])
    program << S(qubits[1]).control([qubits[0]])
    program << H(qubits[1])
    program << H(qubits[1])
    try:
        machine.directly_run(program)
        return program
    finally:
        machine.finalize()
