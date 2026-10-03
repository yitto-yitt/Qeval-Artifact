# EVAL_META: task_id=90, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, X, H

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
atexit.register(lambda: machine.finalize())


def create_custom_controlled():
    custom = QCircuit()
    custom << X(qubits[1]) << H(qubits[2])

    circuit = QCircuit()
    circuit << custom.control([qubits[0], qubits[3]])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
