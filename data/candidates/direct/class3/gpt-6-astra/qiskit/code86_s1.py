# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions


def collect_linear_blocks_with_and_without_limit():
    circuit = QuantumCircuit(5)
    circuit.h(0)
    for qubit in range(4):
        circuit.cx(qubit, qubit + 1)

    unrestricted = PassManager(CollectLinearFunctions()).run(circuit)
    restricted = PassManager(
        CollectLinearFunctions(max_block_width=3)
    ).run(circuit)

    return unrestricted, restricted
