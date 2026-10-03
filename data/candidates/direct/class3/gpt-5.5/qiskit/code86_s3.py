# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions


def collect_linear_blocks_with_and_without_limit():
    circuit = QuantumCircuit(5)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.cx(2, 3)
    circuit.cx(3, 4)

    circuit_no_limit = PassManager([CollectLinearFunctions()]).run(circuit)
    circuit_limited = PassManager([CollectLinearFunctions(max_block_width=3)]).run(circuit)

    return circuit_no_limit, circuit_limited
