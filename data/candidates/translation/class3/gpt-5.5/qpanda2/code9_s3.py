# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)

def create_efficientSU2():
    try:
        theta = [var(0.0, True) for _ in range(12)]
        RY(qubits[0], theta[0])
    except Exception:
        theta = [0.0 for _ in range(12)]

    circuit = QCircuit()

    for i in range(3):
        circuit.insert(RY(qubits[i], theta[i]))
    for i in range(3):
        circuit.insert(RZ(qubits[i], theta[3 + i]))

    barrier_fn = globals().get("BARRIER", None) or globals().get("Barrier", None)
    if barrier_fn is not None:
        try:
            circuit.insert(barrier_fn(qubits))
        except Exception:
            try:
                for q in qubits:
                    circuit.insert(barrier_fn(q))
            except Exception:
                pass

    circuit.insert(CNOT(qubits[2], qubits[1]))
    circuit.insert(CNOT(qubits[1], qubits[0]))

    if barrier_fn is not None:
        try:
            circuit.insert(barrier_fn(qubits))
        except Exception:
            try:
                for q in qubits:
                    circuit.insert(barrier_fn(q))
            except Exception:
                pass

    for i in range(3):
        circuit.insert(RY(qubits[i], theta[6 + i]))
    for i in range(3):
        circuit.insert(RZ(qubits[i], theta[9 + i]))

    return circuit
