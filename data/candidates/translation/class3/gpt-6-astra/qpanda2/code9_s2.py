# EVAL_META: task_id=9, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)


def create_efficientSU2():
    circuit = pq.VariationalQuantumCircuit()
    parameters = [pq.var(0.0, True) for _ in range(12)]

    for layer in range(2):
        offset = 6 * layer
        for i in range(3):
            circuit.insert(
                pq.VariationalQuantumGate_RY(qubits[i], parameters[offset + i])
            )
        for i in range(3):
            circuit.insert(
                pq.VariationalQuantumGate_RZ(qubits[i], parameters[offset + 3 + i])
            )

        if layer == 0:
            entanglement = pq.QCircuit()
            entanglement << pq.BARRIER(qubits)
            entanglement << pq.CNOT(qubits[1], qubits[2])
            entanglement << pq.CNOT(qubits[0], qubits[1])
            entanglement << pq.BARRIER(qubits)
            circuit.insert(pq.VariationalQuantumCircuit(entanglement))

    program = pq.QProg()
    program << circuit.feed()
    machine.directly_run(program)
    return circuit
