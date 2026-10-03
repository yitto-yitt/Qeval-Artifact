# EVAL_META: task_id=89, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, H

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_controlled_hgate():
    circuit = QCircuit()
    circuit << H(qubits[2]).control([qubits[0], qubits[1]])
    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
