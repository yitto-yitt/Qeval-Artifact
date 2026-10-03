# EVAL_META: task_id=86, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CollectLinearFunctions


def collect_linear_blocks_with_and_without_limit():
    def build_circuit():
        qc = QuantumCircuit(5)
        qc.h(0)
        for i in range(4):
            qc.cx(i, i + 1)
        return qc

    qc_no_limit = build_circuit()
    pm_no_limit = PassManager(CollectLinearFunctions())
    circuit_no_limit = pm_no_limit.run(qc_no_limit)

    qc_limit = build_circuit()
    pm_limit = PassManager(CollectLinearFunctions(max_block_width=3))
    circuit_limit = pm_limit.run(qc_limit)

    return circuit_no_limit, circuit_limit
