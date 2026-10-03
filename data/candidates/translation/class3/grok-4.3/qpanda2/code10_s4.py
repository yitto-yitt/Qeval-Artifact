# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
def create_operator():
    unitary = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    circuit = pq.QCircuit()
    circuit << pq.QOracle(qubits, unitary)
    optimized = pq.circuit_optimizer(circuit, ["U3", "CNOT"])
    return optimized
machine.finalize()
