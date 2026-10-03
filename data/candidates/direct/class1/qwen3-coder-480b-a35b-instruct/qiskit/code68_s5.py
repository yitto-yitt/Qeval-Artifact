# EVAL_META: task_id=68, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    """
    Implements the Zeno version of the Elitzur-Vaidman bomb tester with 25 cycles.
    
    Args:
        bomb_live (bool): Whether the bomb is live (True) or a dud (False)
        
    Returns:
        dict: A dictionary containing the probability distribution with keys
              'live_predictions', 'dud_predictions', and 'detonations'
    """
    # Number of cycles
    n_cycles = 25
    
    # Create quantum circuit
    qc = QuantumCircuit(2, 1)  # 2 qubits (probe and bomb), 1 classical bit
    
    # Initialize probe qubit to |0>
    # Bomb qubit will be |0> if dud, |1> if live initially
    if bomb_live:
        qc.x(1)  # Set bomb qubit to |1> if live
    
    # Small rotation angle for each cycle
    theta = math.pi / 2 / n_cycles
    
    # Counter for detonations
    detonation_count = 0
    simulation_shots = 10000  # Use multiple shots to get probability estimates
    
    simulator = AerSimulator()
    
    # Run multiple simulations to estimate probabilities
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    for _ in range(simulation_shots):
        # Reset the circuit for each shot
        qc_temp = QuantumCircuit(2, 1)
        
        # Initialize as before
        if bomb_live:
            qc_temp.x(1)  # Set bomb qubit to |1> if live
        
        # Apply n_cycles of the Zeno protocol
        for i in range(n_cycles):
            # Apply small rotation on probe qubit
            qc_temp.ry(theta, 0)
            
            # CNOT gate - if bomb is live (|1>) and probe is |1>, it might detonate
            # In quantum simulation, we'll model this by checking state after rotation
            # If bomb is live and probe becomes excited, there's a chance of detonation
            
            # For simulation purposes, we implement interaction between probe and bomb
            # If bomb is live (qubit 1 is |1>) and probe (qubit 0) has some amplitude in |1>,
            # then there's a possibility of detonation
            qc_temp.cx(0, 1)  # Interaction: if probe is |1> and bomb is |1>, bomb state changes
            
            # Measure bomb qubit to check for detonation
            qc_temp.measure(1, 0)
            
            # Simulate the measurement result
            backend = AerSimulator()
            job = backend.run(qc_temp, shots=1)
            result = job.result()
            counts = result.get_counts()
            
            # Get the measured value
            measured_result = list(counts.keys())[0]  # Get the measurement outcome
            measured_value = int(measured_result)
            
            # If bomb was originally live and we measure |1> on bomb qubit, it means no detonation yet
            # If we measure |0> on bomb qubit when it was originally live, it indicates detonation occurred during evolution
            if bomb_live:
                # If bomb was live originally and now measures 0, it may have detonated
                # Actually, in our setup: if bomb was |1> initially and remains |1>, no detonation
                # If bomb was |1> initially and becomes |0>, detonation happened
                original_bomb_state = 1
                if measured_value == 0 and original_bomb_state == 1:
                    detonations += 1
                    break
                elif measured_value == 1 and original_bomb_state == 1:
                    # No detonation, continue
                    pass
            else:
                # Bomb was originally a dud (|0>)
                # If it remains |0>, it's still a dud
                # If it becomes |1>, that would indicate an error in our model
                pass
                
            # Reset for next iteration without changing bomb state permanently in the conceptual model
            # We'll recreate the circuit each time conceptually
            pass
    
    # More accurate simulation approach
    # Let's properly simulate the quantum evolution
    prob_detonation = 0.0
    if bomb_live:
        # Probability of detecting live bomb without detonation after n cycles
        # Each cycle has prob ~ (theta^2/4) of causing detonation if bomb is live
        # After n cycles: prob_detonation_per_cycle = sin^2(theta/2) ~ (theta/2)^2 for small theta
        # Total prob of detonation = 1 - (cos(theta/2))^(2*n_cycles)
        small_rotation_prob_detonation = math.sin(theta/2)**2
        prob_no_detonation_all_cycles = (math.cos(theta/2))**(2*n_cycles)
        prob_detonation = 1 - prob_no_detonation_all_cycles
    else:
        # If bomb is a dud, no detonation possible
        prob_detonation = 0.0
    
    # When no detonation occurs and bomb is live, we can sometimes identify it as live
    if bomb_live:
        # Probability of correctly identifying a live bomb without detonation
        # This happens when final state of probe qubit indicates presence of bomb
        prob_success_identify_live = ((math.cos(theta/2))**(2*n_cycles)) * (1 - math.cos(theta)**2)  # Approximate
        prob_remaining_probe_0 = (math.cos(theta/2))**(2*n_cycles)
        prob_live_prediction = prob_remaining_probe_0 * math.sin(theta)**2  # Rough approximation
        
        # Better calculation:
        # After n rotations of angle theta, amplitude on |1> state of probe is ~ sin(n*theta)/n 
        # Actually, with weak measurements, it's more complex
        # For Zeno effect with n cycles of angle pi/(2n), final prob of detection is ~ 1/n^2
        prob_dud_prediction_if_live = (math.cos(math.pi/(2*n_cycles)))**(2*n_cycles)  # Goes to 1/e^(pi^2/4) as n->inf
        prob_live_detected = 1 - prob_dud_prediction_if_live
        
        # Simplified correct calculation:
        prob_detonation = 1 - (math.cos(math.pi/(2*n_cycles))**(2*n_cycles))
        prob_no_detonation = (math.cos(math.pi/(2*n_cycles))**(2*n_cycles))
        
        # Of the no-detonation cases, what fraction correctly identifies live vs dud?
        # For live bomb: after n cycles, probe state is rotated but bomb affects it
        # The success probability for detecting live bomb without detonation approaches 1 as n increases
        prob_live_prediction = prob_no_detonation * 1.0  # Most non-detonations correctly identify live bomb
        prob_dud_prediction = 0.0  # Because bomb is actually live
    else:
        # Bomb is dud
        prob_detonation = 0.0
        # When bomb is dud, probe evolves as if there's no bomb, ending up in |1> state
        # So we always correctly predict it's a dud
        prob_dud_prediction = 1.0
        prob_live_prediction = 0.0
    
    # More precise calculation for the actual algorithm
    if bomb_live:
        # Probability of detonation over all cycles
        # Each cycle has a small chance to detonate if bomb is live
        # P(detonation in one cycle) ≈ sin²(θ/2) where θ = π/(2*n_cycles)
        # For small angles, sin²(θ/2) ≈ (θ/2)²
        # Total detonation probability after n cycles ≈ n * (θ/2)² = n * (π/4n_cycles)² = n * π²/(16*n_cycles²)
        # Actually, it's 1 - cos^n(θ) ≈ 1 - (1 - θ²/2)^n ≈ 1 - exp(-n*θ²/2) for small θ
        theta = math.pi / (2 * n_cycles)
        prob_detonation = 1 - (math.cos(theta) ** n_cycles)
        
        # Probability of no detonation
        prob_no_detonation = (math.cos(theta) ** n_cycles)
        
        # Of the no-detonation cases, what fraction results in correct live prediction?
        # After n cycles with live bomb, the probe qubit will have a different phase/wavefunction
        # that allows us to infer the presence of the bomb
        # The success probability approaches 1 as n -> infinity (Zeno effect)
        # For finite n, it's approximately 1 - cos^n(θ)
        prob_live_prediction = prob_no_detonation  # Most of the non-detected cases correctly identify live bomb
        prob_dud_prediction = 0.0
    else:
        # If bomb is dud, no detonation possible
        prob_detonation = 0.0
        # We always correctly identify dud bombs in this setup
        prob_dud_prediction = 1.0
        prob_live_prediction = 0.0
    
    return {
        'live_predictions': prob_live_prediction,
        'dud_predictions': prob_dud_prediction,
        'detonations': prob_detonation
    }
