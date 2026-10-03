# EVAL_META: task_id=130, framework=qpanda2, class=3
import atexit
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)

def inv_circuit(n):
    n = operator.index(n)
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    circuit << pq.I(qubits[0])
    for i in range(5, n):
        circuit << pq.I(qubits[i])

    for i in range(2):
        circuit << pq.H(qubits[i + 1])

    for i in range(2):
        circuit << pq.CNOT(qubits[i + 1], qubits[i + 3])

    return circuit.dagger()

atexit.register(lambda: machine.finalize())
