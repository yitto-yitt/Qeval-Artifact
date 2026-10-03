# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions


def collect_linear_blocks_with_and_without_limit():
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)

    pm_unlimited = PassManager([CollectLinearFunctions()])
    unlimited = pm_unlimited.run(qc)

    pm_limited = PassManager([CollectLinearFunctions(max_block_width=3)])
    limited = pm_limited.run(qc)

    return unlimited, limited
