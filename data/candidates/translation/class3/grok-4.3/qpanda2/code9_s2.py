# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
def create_efficientSU2():
    circuit = pq.QCircuit()
    params = [pq.var(str(i)) for i in range(12)]
    for i in range(3):
        circuit.insert(pq.RY(qubits[i], params[2*i]))
        circuit.insert(pq.RZ(qubits[i], params[2*i+1]))
    circuit.insert(pq.Barrier(qubits))
    circuit.insert(pq.CNOT(qubits[2], qubits[1]))
    circuit.insert(pq.CNOT(qubits[1], qubits[0]))
    circuit.insert(pq.Barrier(qubits))
    for i in range(3):
        circuit.insert(pq.RY(qubits[i], params[6 + 2*i]))
        circuit.insert(pq.RZ(qubits[i], params[6 + 2*i + 1]))
    return circuit
machine.finalize()
