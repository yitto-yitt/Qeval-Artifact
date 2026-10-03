# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions


def collect_linear_blocks_with_and_without_limit():
    circuit = QuantumCircuit(5)
    circuit.h(0)
    for i in range(4):
        circuit.cx(i, i + 1)

    without_limit = PassManager([CollectLinearFunctions()]).run(circuit)
    with_limit = PassManager([CollectLinearFunctions(max_block_width=3)]).run(circuit)

    return without_limit, with_limit
