# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *
from pyqpanda3.utils import *


def calculate_phase_difference_fidelity():
    # Create the first operator (Hadamard gate)
    op_a = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    
    # Create the second operator (Hadamard gate with global phase)
    phase_factor = np.exp(1j * 0.5)
    op_b = phase_factor * op_a
    
    # Convert to QPanda operators
    operator_a = QOperator(op_a)
    operator_b = QOperator(op_b)
    
    # Calculate process fidelity
    fidelity = operator_a.process_fidelity(operator_b)
    
    return fidelity
