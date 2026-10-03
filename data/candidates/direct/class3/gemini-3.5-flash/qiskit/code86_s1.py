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
    
    # Pass manager with no block width restriction
    pm_no_limit = PassManager(CollectLinearFunctions())
    qc_no_limit = pm_no_limit.run(qc)
    
    # Pass manager with max_block_size of 3
    pm_limit = PassManager(CollectLinearFunctions(max_block_size=3))
    qc_limit = pm_limit.run(qc)
    
    return qc_no_limit, qc_limit
