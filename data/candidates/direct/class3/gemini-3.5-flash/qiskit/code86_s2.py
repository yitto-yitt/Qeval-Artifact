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
    
    # 1. One with no block width restriction (default)
    pm1 = PassManager(CollectLinearFunctions())
    qc1 = pm1.run(qc)
    
    # 2. One with a max_block_width of 3 (using max_block_size parameter)
    pm2 = PassManager(CollectLinearFunctions(max_block_size=3))
    qc2 = pm2.run(qc)
    
    return qc1, qc2
