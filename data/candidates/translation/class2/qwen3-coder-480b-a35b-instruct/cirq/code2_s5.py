# EVAL_META: task_id=2, framework=cirq, class=2
import cirq
import numpy as np


def create_bell_statevector():
    # Create the |00⟩ and |11⟩ states
    zero_zero = cirq.StateVectorSimulationState(
        initial_state_vector=np.array([1, 0, 0, 0], dtype=complex),
        qubits=[cirq.LineQubit(0), cirq.LineQubit(1)]
    ).target_tensor
    
    one_one = cirq.StateVectorSimulationState(
        initial_state_vector=np.array([0, 0, 0, 1], dtype=complex),
        qubits=[cirq.LineQubit(0), cirq.LineQubit(1)]
    ).target_tensor
    
    # Create the Phi+ Bell state: (|00⟩ + |11⟩) / sqrt(2)
    bell_state = (zero_zero + one_one) / np.sqrt(2)
    
    return bell_state
