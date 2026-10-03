# EVAL_META: task_id=10, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)


def create_operator():
    circuit = QCircuit()
    circuit << X(qubits[0]) << X(qubits[1])
    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
