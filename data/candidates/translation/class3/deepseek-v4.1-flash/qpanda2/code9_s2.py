# EVAL_META: task_id=9, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = pq.QCircuit()
    for q in qubits:
        circuit << pq.RY(q, 0.0)
        circuit << pq.RZ(q, 0.0)
    circuit << pq.QBarrier(qubits)
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.CNOT(qubits[0], qubits[2])
    circuit << pq.CNOT(qubits[1], qubits[2])
    circuit << pq.QBarrier(qubits)
    for q in qubits:
        circuit << pq.RY(q, 0.0)
        circuit << pq.RZ(q, 0.0)
    circuit << pq.QBarrier(qubits)
    return circuit

if __name__ == "__main__":
    machine.finalize()
