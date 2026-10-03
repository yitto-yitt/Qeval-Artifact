# EVAL_META: task_id=118, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_c3sx_circuit():
    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(4)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(4)
    elif hasattr(qvm, "allocate_qubits"):
        qubits = qvm.allocate_qubits(4)
    else:
        qubits = qvm.qAllocMany(4)

    circuit = pq.QCircuit()
    circuit << pq.H(qubits[3])

    if hasattr(pq, "S"):
        s_gate = pq.S(qubits[3])
    elif hasattr(pq, "P"):
        s_gate = pq.P(qubits[3], math.pi / 2)
    else:
        s_gate = pq.U1(qubits[3], math.pi / 2)

    controls = [qubits[0], qubits[1], qubits[2]]
    controlled_s = s_gate.control(controls)
    if controlled_s is None:
        controlled_s = s_gate

    circuit << controlled_s
    circuit << pq.H(qubits[3])

    if not hasattr(create_c3sx_circuit, "_resources"):
        create_c3sx_circuit._resources = []
    create_c3sx_circuit._resources.append((qvm, qubits))

    return circuit
