# EVAL_META: task_id=59, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cz_gate():
    circuit = pq.QCircuit()
    circuit.insert(pq.H(qubits[1]))
    circuit.insert(pq.CNOT(qubits[0], qubits[1]))
    circuit.insert(pq.H(qubits[1]))
    return circuit

machine.finalize()
