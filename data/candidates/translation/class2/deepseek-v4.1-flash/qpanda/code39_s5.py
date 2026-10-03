# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QProg, Qubit, H, CPUQVM
from pyqpanda3.quantum_info import StateVector

def create_uniform_superposition(n):
    prog = QProg()
    qubits = [Qubit(i) for i in range(n)]
    for q in qubits:
        prog << H(q)
    machine = CPUQVM()
    machine.run(prog)
    return StateVector(machine.get_qstate())
