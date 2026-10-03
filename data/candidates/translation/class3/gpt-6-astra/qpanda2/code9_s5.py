# EVAL_META: task_id=9, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_efficientSU2():
    parameters = [pq.var(0.0, True) for _ in range(12)]
    circuit = pq.VariationalQuantumCircuit()

    for i, qubit in enumerate(qubits):
        circuit.insert(pq.VariationalQuantumGate_RY(qubit, parameters[i]))
    for i, qubit in enumerate(qubits):
        circuit.insert(pq.VariationalQuantumGate_RZ(qubit, parameters[3 + i]))

    circuit.insert(pq.BARRIER(qubits))
    circuit.insert(pq.CNOT(qubits[1], qubits[2]))
    circuit.insert(pq.CNOT(qubits[0], qubits[1]))
    circuit.insert(pq.BARRIER(qubits))

    for i, qubit in enumerate(qubits):
        circuit.insert(pq.VariationalQuantumGate_RY(qubit, parameters[6 + i]))
    for i, qubit in enumerate(qubits):
        circuit.insert(pq.VariationalQuantumGate_RZ(qubit, parameters[9 + i]))

    program = pq.QProg()
    program << circuit.feed()
    machine.directly_run(program)
    return circuit


atexit.register(machine.finalize)
