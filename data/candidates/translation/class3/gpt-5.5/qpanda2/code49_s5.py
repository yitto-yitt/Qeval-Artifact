# EVAL_META: task_id=49, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def simple_elitzur_vaidman():
    circuit = pq.QCircuit()
    circuit << pq.H(qubits[0])
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.H(qubits[0])
    return circuit

machine.finalize()
