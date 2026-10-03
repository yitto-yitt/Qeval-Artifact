# EVAL_META: task_id=130, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
atexit.register(lambda: machine.finalize())


def inv_circuit(n):
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    circuit = pq.QCircuit()
    for i in range(2):
        circuit << pq.H(qubits[i + 1])
    for i in range(2):
        circuit << pq.CNOT(qubits[i + 1], qubits[i + 3])

    return circuit.dagger()
