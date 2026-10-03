# EVAL_META: task_id=57, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_swap_gate():
    circuit = pq.QCircuit()
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.CNOT(qubits[1], qubits[0])
    circuit << pq.CNOT(qubits[0], qubits[1])
    return circuit

machine.finalize()
