# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, PassManager, CollectLinearFunctions

def collect_linear_blocks_with_and_without_limit():
    qc_full = QuantumCircuit(5)
    qc_full.h(0)
    qc_full.cx(0, 1)
    qc_full.cx(1, 2)
    qc_full.cx(2, 3)
    qc_full.cx(3, 4)

    qc_limited = QuantumCircuit(5)
    qc_limited.h(0)
    qc_limited.cx(0, 1)
    qc_limited.cx(1, 2)
    qc_limited.cx(2, 3)
    qc_limited.cx(3, 4)

    pm_full = PassManager([CollectLinearFunctions()])
    full_block = pm_full.run(qc_full)

    pm_limited = PassManager([CollectLinearFunctions(max_block_width=3)])
    limited_block = pm_limited.run(qc_limited)

    return full_block, limited_block
