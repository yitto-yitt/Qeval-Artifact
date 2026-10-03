# EVAL_META: task_id=9, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)

def create_efficientSU2():
    theta = [pq.var(0.0, True) for _ in range(12)]
    circuit = pq.VariationalQuantumCircuit()

    for i in range(3):
        circuit.insert(pq.VariationalQuantumGate_RY(qubits[i], theta[i]))
    for i in range(3):
        circuit.insert(pq.VariationalQuantumGate_RZ(qubits[i], theta[3 + i]))

    circuit.insert(pq.VariationalQuantumGate_CNOT(qubits[2], qubits[1]))
    circuit.insert(pq.VariationalQuantumGate_CNOT(qubits[1], qubits[0]))

    for i in range(3):
        circuit.insert(pq.VariationalQuantumGate_RY(qubits[i], theta[6 + i]))
    for i in range(3):
        circuit.insert(pq.VariationalQuantumGate_RZ(qubits[i], theta[9 + i]))

    return circuit
