# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq

def collect_linear_blocks_with_and_without_limit():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(5)
    elif hasattr(machine, "qalloc_many"):
        q = machine.qalloc_many(5)
    elif hasattr(machine, "qAllocMany"):
        q = machine.qAllocMany(5)
    else:
        q = [machine.qAlloc() for _ in range(5)]

    cnot = getattr(pq, "CNOT", None)
    if cnot is None:
        cnot = getattr(pq, "CX")

    full_linear_block = pq.QCircuit()
    full_linear_block << cnot(q[0], q[1])
    full_linear_block << cnot(q[1], q[2])
    full_linear_block << cnot(q[2], q[3])
    full_linear_block << cnot(q[3], q[4])

    full_block = pq.QProg()
    full_block << pq.H(q[0])
    full_block << full_linear_block

    limited_linear_block_1 = pq.QCircuit()
    limited_linear_block_1 << cnot(q[0], q[1])
    limited_linear_block_1 << cnot(q[1], q[2])

    limited_linear_block_2 = pq.QCircuit()
    limited_linear_block_2 << cnot(q[2], q[3])
    limited_linear_block_2 << cnot(q[3], q[4])

    limited_block = pq.QProg()
    limited_block << pq.H(q[0])
    limited_block << limited_linear_block_1
    limited_block << limited_linear_block_2

    if not hasattr(collect_linear_blocks_with_and_without_limit, "_qpanda_refs"):
        collect_linear_blocks_with_and_without_limit._qpanda_refs = []
    collect_linear_blocks_with_and_without_limit._qpanda_refs.append((machine, q))

    return full_block, limited_block
