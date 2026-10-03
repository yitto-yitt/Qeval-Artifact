# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq


def collect_linear_blocks_with_and_without_limit():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()
    elif hasattr(machine, "initQVM"):
        machine.initQVM()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(5)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(5)
    elif hasattr(machine, "allocate_qubits"):
        qubits = machine.allocate_qubits(5)
    elif hasattr(machine, "qAlloc"):
        qubits = [machine.qAlloc() for _ in range(5)]
    else:
        qubits = [machine.qalloc() for _ in range(5)]

    cnot = getattr(pq, "CNOT", getattr(pq, "CX", None))

    full_block = pq.QProg()
    full_block << pq.H(qubits[0])
    full_linear_block = pq.QCircuit()
    full_linear_block << cnot(qubits[0], qubits[1])
    full_linear_block << cnot(qubits[1], qubits[2])
    full_linear_block << cnot(qubits[2], qubits[3])
    full_linear_block << cnot(qubits[3], qubits[4])
    full_block << full_linear_block

    limited_block = pq.QProg()
    limited_block << pq.H(qubits[0])
    limited_linear_block_1 = pq.QCircuit()
    limited_linear_block_1 << cnot(qubits[0], qubits[1])
    limited_linear_block_1 << cnot(qubits[1], qubits[2])
    limited_linear_block_2 = pq.QCircuit()
    limited_linear_block_2 << cnot(qubits[2], qubits[3])
    limited_linear_block_2 << cnot(qubits[3], qubits[4])
    limited_block << limited_linear_block_1
    limited_block << limited_linear_block_2

    collect_linear_blocks_with_and_without_limit._qpanda_machine = machine
    return full_block, limited_block
