# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler.passes import CollectLinearFunctions
from qiskit.transpiler import PassManager


def collect_linear_blocks_with_and_without_limit():
    # Create the initial 5-qubit quantum circuit
    qc = QuantumCircuit(5)
    qc.h(0)
    for i in range(4):
        qc.cx(i, i + 1)

    # Apply CollectLinearFunctions without block width restriction
    pass_manager_no_limit = PassManager(CollectLinearFunctions())
    optimized_circuit_no_limit = pass_manager_no_limit.run(qc)

    # Apply CollectLinearFunctions with max_block_width of 3
    pass_manager_with_limit = PassManager(CollectLinearFunctions(max_block_width=3))
    optimized_circuit_with_limit = pass_manager_with_limit.run(qc)

    return optimized_circuit_no_limit, optimized_circuit_with_limit
