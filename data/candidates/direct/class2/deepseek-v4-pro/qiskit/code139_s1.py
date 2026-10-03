# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix

def schmidt_test(data, qargs_B):
    # Convert input to a pure Statevector if needed
    if isinstance(data, DensityMatrix):
        state = data.to_statevector(atol=1e-10)
    elif isinstance(data, Statevector):
        state = data
    else:
        # Assume array-like
        state = Statevector(data)
    
    # Perform Schmidt decomposition using built-in method
    terms = state.schmidt_decomposition(qargs=qargs_B)
    
    # Each term is (coefficient, Statevector_A, Statevector_B)
    # Convert to list of (coeff, np.array, np.array)
    result = []
    for coeff, sv_a, sv_b in terms:
        result.append((float(coeff), sv_a.data, sv_b.data))
    return result
