# EVAL_META: task_id=4, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)


def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]
    circuit = pq.QCircuit()
    circuit << pq.QOracle(
        qubits, [complex(value) for row in matrix for value in row]
    )
    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
