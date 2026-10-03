# EVAL_META: task_id=0, framework=qpanda2, class=3
import atexit
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(0)


def create_quantum_circuit(n_qubits):
    n_qubits = operator.index(n_qubits)
    if n_qubits < 0:
        raise ValueError("n_qubits must be non-negative")

    while len(qubits) < n_qubits:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
