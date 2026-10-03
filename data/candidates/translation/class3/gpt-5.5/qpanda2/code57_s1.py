# EVAL_META: task_id=57, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def create_swap_gate():
    circuit = pq.QCircuit()
    circuit.insert(pq.CNOT(qubits[0], qubits[1]))
    circuit.insert(pq.CNOT(qubits[1], qubits[0]))
    circuit.insert(pq.CNOT(qubits[0], qubits[1]))
    return circuit
