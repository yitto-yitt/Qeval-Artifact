# EVAL_META: task_id=9, framework=qpanda2, class=3
import atexit
import numpy as np
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

atexit.register(machine.finalize)

def create_efficientSU2():
    def _insert_barrier(circuit):
        barrier = getattr(pq, "BARRIER", None)
        if barrier is not None:
            try:
                circuit.insert(barrier(qubits))
            except Exception:
                pass

    try:
        try:
            theta = [pq.var(0.0, True) for _ in range(12)]
        except Exception:
            theta = [pq.var(np.array([0.0]), True) for _ in range(12)]

        circuit = pq.VariationalQuantumCircuit()

        for i in range(3):
            circuit.insert(pq.VariationalQuantumGate_RY(qubits[i], theta[i]))
        for i in range(3):
            circuit.insert(pq.VariationalQuantumGate_RZ(qubits[i], theta[3 + i]))

        _insert_barrier(circuit)

        circuit.insert(pq.VariationalQuantumGate_CNOT(qubits[1], qubits[2]))
        circuit.insert(pq.VariationalQuantumGate_CNOT(qubits[0], qubits[1]))

        _insert_barrier(circuit)

        for i in range(3):
            circuit.insert(pq.VariationalQuantumGate_RY(qubits[i], theta[6 + i]))
        for i in range(3):
            circuit.insert(pq.VariationalQuantumGate_RZ(qubits[i], theta[9 + i]))

        return circuit

    except Exception:
        theta = [0.0] * 12
        circuit = pq.QCircuit()

        for i in range(3):
            circuit.insert(pq.RY(qubits[i], theta[i]))
        for i in range(3):
            circuit.insert(pq.RZ(qubits[i], theta[3 + i]))

        _insert_barrier(circuit)

        circuit.insert(pq.CNOT(qubits[1], qubits[2]))
        circuit.insert(pq.CNOT(qubits[0], qubits[1]))

        _insert_barrier(circuit)

        for i in range(3):
            circuit.insert(pq.RY(qubits[i], theta[6 + i]))
        for i in range(3):
            circuit.insert(pq.RZ(qubits[i], theta[9 + i]))

        return circuit
