# EVAL_META: task_id=92, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState


def calculate_stabilizer_state_info():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    stabilizer_state = StabilizerState.from_instruction(qc)
    probs = stabilizer_state.probabilities_dict()
    return {str(k): float(v) for k, v in probs.items()}
