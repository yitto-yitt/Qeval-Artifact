# EVAL_META: task_id=57, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_swap_gate():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(2)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(2)
    else:
        qubits = [machine.qAlloc(), machine.qAlloc()]

    circuit = pq.QCircuit()
    cnot = getattr(pq, "CNOT", getattr(pq, "CX", None))

    circuit << cnot(qubits[0], qubits[1])
    circuit << cnot(qubits[1], qubits[0])
    circuit << cnot(qubits[0], qubits[1])

    if not hasattr(create_swap_gate, "_resources"):
        create_swap_gate._resources = []
    create_swap_gate._resources.append((machine, qubits))

    return circuit
