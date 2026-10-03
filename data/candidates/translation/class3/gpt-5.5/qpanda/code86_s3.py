# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq

def collect_linear_blocks_with_and_without_limit():
    h_gate = pq.H
    cnot_gate = getattr(pq, "CNOT", None)
    if cnot_gate is None:
        cnot_gate = getattr(pq, "CX")

    machine = None
    try:
        q = list(range(5))
        h_gate(q[0])
        cnot_gate(q[0], q[1])
    except Exception:
        machine = pq.CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        if hasattr(machine, "qAlloc_many"):
            q = machine.qAlloc_many(5)
        else:
            q = [machine.qAlloc() for _ in range(5)]

    def make_linear_block(edges):
        block = pq.QCircuit()
        for control, target in edges:
            block << cnot_gate(q[control], q[target])
        return block

    full_block = pq.QProg()
    full_block << h_gate(q[0])
    full_block << make_linear_block([(0, 1), (1, 2), (2, 3), (3, 4)])

    limited_block = pq.QProg()
    limited_block << h_gate(q[0])
    limited_block << make_linear_block([(0, 1), (1, 2)])
    limited_block << make_linear_block([(2, 3), (3, 4)])

    if machine is not None:
        collect_linear_blocks_with_and_without_limit._machine = machine

    return full_block, limited_block
