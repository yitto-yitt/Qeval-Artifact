# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions


def collect_linear_blocks_with_and_without_limit():
    """Create a 5-qubit circuit and collect linear blocks twice."""
    qc = QuantumCircuit(5)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.cx(2, 3)
    qc.cx(3, 4)

    unlimited_pm = PassManager(CollectLinearFunctions())
    limited_pm = PassManager(CollectLinearFunctions(max_block_width=3))

    unlimited_circuit = unlimited_pm.run(qc)
    limited_circuit = limited_pm.run(qc)

    return unlimited_circuit, limited_circuit
