# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq
import math
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def create_operator():
    circuit = pq.QCircuit()
    circuit << pq.U(qubits[0], math.pi, 0, math.pi) << pq.U(qubits[1], math.pi, 0, math.pi)
    return circuit
machine.finalize()
