# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import math
import atexit

machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(20)

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qubits = global_qubits[:n]
    complex_diag = [complex(x) for x in diag]
    circuit = pq.QCircuit()
    gate = pq.DiagonalGate(qubits, complex_diag)
    circuit.insert(gate)
    return circuit

atexit.register(machine.finalize)
