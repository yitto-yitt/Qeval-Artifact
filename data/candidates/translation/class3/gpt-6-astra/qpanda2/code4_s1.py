# EVAL_META: task_id=4, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, QOracle

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    circuit = QCircuit()
    circuit << QOracle(qubits, [complex(value) for row in matrix for value in row])
    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
