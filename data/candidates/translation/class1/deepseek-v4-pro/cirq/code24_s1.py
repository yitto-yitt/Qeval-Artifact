# EVAL_META: task_id=24, framework=cirq, class=1
import cirq
import numpy as np

def dj_algorithm(oracle):
    """
    oracle: a cirq.Circuit that acts as a Deutsch-Jozsa oracle.
    The circuit contains all qubits; the last qubit is the output.
    Returns a dictionary of probability distribution over input-bitstrings.
    """
    # Retrieve all qubits from the oracle, sort them to have a consistent order
    qubits = sorted(oracle.all_qubits())
    n = len(qubits)
    if n <= 1:
        # The input register has zero qubits, so there is only the constant output.
        return {'': 1.0}

    # Build the Deutsch-Jozsa circuit on the same qubits
    qc = cirq.Circuit()

    # Prepare the output qubit in |1> state, others in |0> (default)
    qc.append(cirq.X(qubits[-1]))
    # Apply Hadamard to all qubits
    qc.append(cirq.H.on_each(*qubits))
    # Append the oracle
    qc += oracle
    # Apply Hadamard again
    qc.append(cirq.H.on_each(*qubits))

    # Simulate to obtain the final state vector (no measurements)
    sim = cirq.Simulator()
    result = sim.simulate(qc)
    state_vector = result.final_state_vector

    # Compute exact probabilities for the input register (all qubits except the last)
    input_bitwidth = n - 1
    probs = {}
    for i in range(1 << input_bitwidth):
        bitstring = format(i, '0{}b'.format(input_bitwidth))
        prob = 0.0
        for anc in (0, 1):
            # Index in state vector: input bits (MSB to LSB) then ancilla (LSB)
            # So i << 1 shifts the input integer left by one, then adds anc.
            idx = (i << 1) + anc
            prob += np.abs(state_vector[idx]) ** 2
        # Skip zero-probability entries to keep the dictionary small (optional)
        if prob > 0:
            probs[bitstring] = prob

    return probs
