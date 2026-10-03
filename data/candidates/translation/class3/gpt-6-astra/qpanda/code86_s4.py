# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq


def collect_linear_blocks_with_and_without_limit():
    block_type = getattr(pq, "QCircuit", pq.QProg)

    full_linear_block = block_type()
    for control in range(4):
        full_linear_block << pq.CNOT(control, control + 1)

    full_block = pq.QProg()
    full_block << pq.H(0)
    full_block << full_linear_block

    limited_block = pq.QProg()
    limited_block << pq.H(0)
    for start in (0, 2):
        linear_block = block_type()
        linear_block << pq.CNOT(start, start + 1)
        linear_block << pq.CNOT(start + 1, start + 2)
        limited_block << linear_block

    simulator = pq.CPUQVM()
    simulator.run(full_block, 1)
    simulator.run(limited_block, 1)

    return full_block, limited_block
