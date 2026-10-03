# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions

def collect_linear_blocks_with_and_without_limit():
    # Create a 5-qubit quantum circuit
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)
    
    # 1. No block width restriction (default)
    pass_no_limit = CollectLinearFunctions()
    pm_no_limit = PassManager(pass_no_limit)
    qc_no_limit = pm_no_limit.run(qc)
    
    # 2. Max block width of 3
    pass_limit_3 = CollectLinearFunctions(max_block_width=3)
    pm_limit_3 = PassManager(pass_limit_3)
    qc_limit_3 = pm_limit_3.run(qc)
    
    return qc_no_limit, qc_limit_3
