# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions

def collect_linear_blocks_with_and_without_limit():
    qc = QuantumCircuit(5)
    qc.h(0)
    for i in range(4):
        qc.cx(i, i + 1)
    pm_unrestricted = PassManager(CollectLinearFunctions())
    circ_unrestricted = pm_unrestricted.run(qc)
    pm_limited = PassManager(CollectLinearFunctions(max_block_width=3))
    circ_limited = pm_limited.run(qc)
    return circ_unrestricted, circ_limited
