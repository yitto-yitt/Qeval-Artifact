# EVAL_META: task_id=130, framework=qpanda2, class=3
import atexit
import operator
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
atexit.register(machine.finalize)


def inv_circuit(n):
    n = operator.index(n)
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    while len(qubits) < n:
        qubits.append(machine.qAlloc())

    circuit = pq.QCircuit()
    for i in range(n):
        if i == 0 or i >= 5:
            circuit << pq.I(qubits[i])

    circuit << pq.H(qubits[1])
    circuit << pq.H(qubits[2])
    circuit << pq.CNOT(qubits[1], qubits[3])
    circuit << pq.CNOT(qubits[2], qubits[4])

    return circuit.dagger()
