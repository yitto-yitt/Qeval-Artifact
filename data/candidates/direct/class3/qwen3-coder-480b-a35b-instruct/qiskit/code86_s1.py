# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions

def collect_linear_blocks_with_and_without_limit():
    # Create the initial 5-qubit circuit
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)
    
    # Create pass manager without block width restriction
    pm_no_limit = PassManager([CollectLinearFunctions()])
    qc_no_limit = pm_no_limit.run(qc)
    
    # Create pass manager with max_block_width=3
    pm_with_limit = PassManager([CollectLinearFunctions(max_block_width=3)])
    qc_with_limit = pm_with_limit.run(qc)
    
    return qc_no_limit, qc_with_limit
