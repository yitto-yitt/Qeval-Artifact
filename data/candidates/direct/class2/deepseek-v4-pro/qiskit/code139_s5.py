# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import DensityMatrix

def schmidt_test(data, qargs_B):
    """Return the Schmidt decomposition for a pure density matrix."""
    rho = DensityMatrix(data)
    psi = rho.to_statevector()
    return psi.schmidt_decomposition(qargs_B)
