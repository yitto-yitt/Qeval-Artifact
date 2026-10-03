# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, UnitaryDecomposer, init_qvm

def decompose_unitary(unitary):
    if not hasattr(decompose_unitary, "_initialized"):
        init_qvm()
        decompose_unitary._initialized = True
    decomposer = UnitaryDecomposer()
    result = decomposer.decompose(unitary, 2)
    if isinstance(result, QCircuit):
        return result
    circuit = QCircuit()
    circuit << result
    return circuit
