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
    pm_no_limit = PassManager(CollectLinearFunctions())
    circ_no_limit = pm_no_limit.run(qc)
    pm_limit = PassManager(CollectLinearFunctions(max_block_width=3))
    circ_limit = pm_limit.run(qc)
    return circ_no_limit, circ_limit
