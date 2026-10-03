# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = pq.qAlloc_many(2)
    circuit = pq.QCircuit()
    circuit << pq.X(qubits[0])
    return circuit
