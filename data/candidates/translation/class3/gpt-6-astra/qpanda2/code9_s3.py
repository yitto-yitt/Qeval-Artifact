# EVAL_META: task_id=9, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(lambda: machine.finalize())


def create_efficientSU2():
    parameters = [pq.var(0.0, True) for _ in range(12)]
    circuit = pq.VariationalQuantumCircuit()

    for layer in range(2):
        offset = 6 * layer
        for index in range(3):
            circuit.insert(
                pq.VariationalQuantumGate_RY(
                    qubits[index], parameters[offset + index]
                )
            )
        for index in range(3):
            circuit.insert(
                pq.VariationalQuantumGate_RZ(
                    qubits[index], parameters[offset + 3 + index]
                )
            )

        if layer == 0:
            barrier = pq.QCircuit()
            barrier.insert(pq.BARRIER(qubits))
            circuit.insert(pq.VariationalQuantumCircuit(barrier))

            circuit.insert(
                pq.VariationalQuantumGate_CNOT(qubits[1], qubits[2])
            )
            circuit.insert(
                pq.VariationalQuantumGate_CNOT(qubits[0], qubits[1])
            )

            barrier = pq.QCircuit()
            barrier.insert(pq.BARRIER(qubits))
            circuit.insert(pq.VariationalQuantumCircuit(barrier))

    program = pq.QProg()
    program.insert(circuit.feed())
    machine.directly_run(program)
    return circuit
