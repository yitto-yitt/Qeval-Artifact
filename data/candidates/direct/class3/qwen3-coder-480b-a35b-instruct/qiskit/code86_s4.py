# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler.passes import CollectLinearFunctions
from qiskit.transpiler import PassManager


def collect_linear_blocks_with_and_without_limit():
    # Create initial circuit
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)

    # Apply CollectLinearFunctions without block width restriction
    pass_manager_no_limit = PassManager(CollectLinearFunctions())
    circuit_no_limit = pass_manager_no_limit.run(qc)

    # Apply CollectLinearFunctions with max_block_width of 3
    pass_manager_with_limit = PassManager(CollectLinearFunctions(max_block_width=3))
    circuit_with_limit = pass_manager_with_limit.run(qc)

    return circuit_no_limit, circuit_with_limit
