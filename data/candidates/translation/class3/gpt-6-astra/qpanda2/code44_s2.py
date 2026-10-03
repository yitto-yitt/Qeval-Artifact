# EVAL_META: task_id=44, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, X, RY

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)


def tensor_circuits():
    circuit = QCircuit()
    circuit << X(qubits[0])
    circuit << RY(qubits[2], 0.2).control([qubits[1]])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
