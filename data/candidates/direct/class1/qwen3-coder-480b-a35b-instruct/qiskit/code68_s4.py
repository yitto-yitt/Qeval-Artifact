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
    
    # Create quantum registers
    bomb_qubit = QuantumRegister(1, name='bomb')
    probe_qubit = QuantumRegister(1, name='probe')
    classical_bits = ClassicalRegister(2, name='c')
    
    qc = QuantumCircuit(bomb_qubit, probe_qubit, classical_bits)
    
    # Initialize the bomb qubit based on whether it's live or not
    if bomb_live:
        # If bomb is live, we represent it as |1> initially
        qc.x(bomb_qubit[0])
    
    # Apply small rotation to probe qubit - angle is pi/(2*n_cycles)
    theta = math.pi / (2 * n_cycles)
    
    for i in range(n_cycles):
        # Apply small rotation to probe qubit
        qc.ry(theta, probe_qubit[0])
        
        # If bomb is live, apply CNOT between probe and bomb
        # This simulates the interaction where the bomb might explode
        if bomb_live:
            qc.cx(probe_qubit[0], bomb_qubit[0])
            
            # Measure bomb qubit after each cycle to check for explosion
            qc.measure(bomb_qubit[0], classical_bits[1])
            
            # Reset bomb qubit if it was measured as |1> (meaning it exploded)
            # In simulation, we'll just continue but track if it would have exploded
            qc.reset(bomb_qubit[0])
        else:
            # If bomb is a dud, no interaction happens
            pass
    
    # After all cycles, measure the probe qubit to determine result
    qc.measure(probe_qubit[0], classical_bits[0])
    
    # Run the circuit
    simulator = AerSimulator()
    shots = 10000  # Use sufficient shots for good statistics
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)
    
    # Process results
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    for outcome, count in counts.items():
        # Outcome format is 'cb' where c is probe measurement and b is bomb measurement
        probe_result = int(outcome[0])  # First bit is probe measurement
        
        if bomb_live:
            # For live bomb case, we need to check if bomb exploded during process
            # In our simulation, any time the bomb qubit was involved in an operation,
            # there's a chance it could have been triggered by the probe being in |1>
            
            # For Zeno effect: With many small rotations, if bomb is live,
            # the probe remains close to |0> state, so measuring |1> indicates live bomb
            if probe_result == 1:
                live_predictions += count
            else:
                dud_predictions += count
            
            # Calculate detonation probability for live bomb case
            # Probability of not detecting bomb in all cycles = (cos(theta))^(2*n_cycles)
            # Probability of detonation = 1 - (cos(theta))^(2*n_cycles)
            prob_no_detonation = (math.cos(theta)) ** (2 * n_cycles)
            prob_detonation = 1 - prob_no_detonation
            
            detonations = int(shots * prob_detonation)
        else:
            # For dud bomb case, there's no interaction, so no detonations possible
            if probe_result == 0:
                dud_predictions += count
            else:
                # Due to quantum randomness, there's still a small chance of getting |1>
                live_predictions += count
    
    # Normalize to get probabilities
    total_shots = shots
    prob_live_pred = live_predictions / total_shots
    prob_dud_pred = dud_predictions / total_shots
    prob_detonation = detonations / total_shots if bomb_live else 0
    
    # For a more accurate theoretical calculation specific to the Zeno EV setup:
    if bomb_live:
        # In the Zeno version, the probability of detecting a live bomb without detonating it
        # increases with number of cycles while keeping detonation probability low
        theta_total = math.pi / 2  # Total rotation should approach pi/2
        # Probability of detecting live bomb (probe=1) without detonation
        prob_live_detected = (math.sin(theta_total / n_cycles) ** 2) * n_cycles  # Simplified approximation
        # Actual detonation probability decreases with more cycles in Zeno scheme
        prob_detonation_actual = 1 - (math.cos(theta)) ** (2 * n_cycles)
        # Remaining probability goes to "missed detection" which we consider as predicting dud
        prob_dud_pred_actual = 1 - prob_live_detected - prob_detonation_actual
        
        # Scale these probabilities according to our simulation
        actual_live_detected = 0
        actual_detonated = 0
        actual_dud_pred = 0
        
        # Simulate the expected outcomes based on theory
        for _ in range(shots):
            import random
            rand_val = random.random()
            
            if rand_val < ((math.sin(theta)) ** 2):  # Live detected
                actual_live_detected += 1
            elif rand_val < ((math.sin(theta)) ** 2) + (1 - (math.cos(theta)) ** 2):  # Detonated
                actual_detonated += 1
            else:  # Predicted dud
                actual_dud_pred += 1
                
        return {
            'live_predictions': actual_live_detected / shots,
            'dud_predictions': actual_dud_pred / shots,
            'detonations': actual_detonated / shots
        }
    else:
        # For dud bomb, no detonations possible
        # Measurement of probe qubit gives probabilistic results
        prob_probe_one = (math.sin(theta) ** 2) * n_cycles  # Approximation
        if prob_probe_one > 1.0:
            prob_probe_one = 1.0 - (math.cos(theta) ** (2 * n_cycles))
        
        prob_probe_zero = 1.0 - prob_probe_one
        
        return {
            'live_predictions': prob_probe_one,
            'dud_predictions': prob_probe_zero,
            'detonations': 0.0
        }

    # More precise implementation
    theta = math.pi / (2 * n_cycles)
    
    if bomb_live:
        # Probability that bomb explodes at some point during n cycles
        # Each cycle has a small probability of detonation if bomb is live and probe rotates to |1>
        # P(detonation in one cycle) ≈ sin²(θ) when bomb is live
        # But actually it's more complex due to quantum evolution
        
        # For the Zeno version of EV bomb tester:
        # After n cycles with small angle θ = π/(2n), 
        # the probability of successfully identifying a live bomb without detonation approaches 1
        # while the probability of detonation approaches 0 as n increases
        
        # Probability of NOT detonating in all cycles (for live bomb)
        prob_not_detonated = (math.cos(theta)) ** (2 * n_cycles)
        prob_detonated = 1 - prob_not_detonated
        
        # When not detonated, the probe qubit will be in a state that allows us to infer
        # whether the bomb was live or not
        # If live bomb doesn't detonate, we can detect it with high probability
        prob_correctly_identified_as_live = (math.sin(theta)) ** 2  # per cycle contribution
        
        # For n cycles, if bomb is live and didn't explode, we predict it correctly most of the time
        prob_live_predicted_if_not_detonated = 1 - (math.cos(theta)) ** (2 * n_cycles)
        
        live_predictions = (1 - prob_detonated) * prob_live_predicted_if_not_detonated
        dud_predictions = (1 - prob_detonated) * (1 - prob_live_predicted_if_not_detonated)
        detonations = prob_detonated
    else:
        # If bomb is a dud, no detonation possible
        # The probe qubit evolves freely, and we measure it
        # Since bomb is dud, no interaction occurs, so final state depends on total rotation
        # After n cycles of angle θ, total rotation is n*θ = π/2
        # So probe starts from |0>, after π/2 rotation around Y becomes (|0>+|1>)/sqrt(2)
        # Measuring gives 50% |0> and 50% |1>
        
        # Actually, in each cycle with dud, probe rotates by θ
        # After n cycles: amplitude of |1> = sin(n*θ) where n*θ = π/2
        # So final state of probe is approximately |1> with high probability
        # Wait, let me recalculate: each cycle adds a small rotation θ
        # After n cycles with dud: the probe has rotated n*θ = π/2 total
        # So it goes from |0> to |1> completely
        # Therefore we'd always measure |1> and incorrectly think it's live
        
        # No, that's wrong. Each rotation is ry(θ), so after one step:
        # |0> -> cos(θ)|0> + sin(θ)|1>
        # After second step: ry(θ)(cos(θ)|0> + sin(θ)|1>) 
        # This continues, and after n steps with θ_total = n*θ = π/2,
        # we go from |0> to approximately |1>
        
        # For dud bomb, probe ends up near |1>, so we predict live
        prob_probe_final_1 = (math.sin(math.pi/2))**2  # = 1
        prob_probe_final_0 = (math.cos(math.pi/2))**2  # = 0
        
        live_predictions = prob_probe_final_1  # We incorrectly predict live
        dud_predictions = prob_probe_final_0  # We correctly predict dud
        detonations = 0.0  # Dud cannot detonate
    
    # Correct implementation following the quantum circuit model
    theta = math.pi / (2 * n_cycles)
    
    if bomb_live:
        # For live bomb: probability of detonation decreases with more cycles in Zeno regime
        # The survival probability (not detonating) is approximately cos^n(θ) for large n
        # But more accurately, probability of surviving all measurements is (cos(θ))^(2*n)
        prob_survive_all = (math.cos(theta)) ** (2 * n_cycles)
        prob_detonate_at_some_point = 1 - prob_survive_all
        
        # Of the cases that survive, how many do we correctly identify as live?
        # When we don't detonate, the probe state has evolved differently than if bomb were dud
        # The conditional probability of measuring probe as 1 (indicating live) given survival
        prob_measure_1_given_survival = (math.sin(theta * n_cycles)) ** 2  # = (sin(π/2))^2 = 1
        
        live_predictions = prob_survive_all * prob_measure_1_given_survival
        dud_predictions = prob_survive_all * (1 - prob_measure_1_given_survival)
        detonations = prob_detonate_at_some_point
    else:
        # For dud bomb: no detonation possible
        # The probe undergoes n rotations of angle θ each, total π/2
        # Final state is essentially |1>, so we measure 1 with probability ~1
        # This means we predict it's live even though it's a dud
        final_angle = n_cycles * theta  # = π/2
        prob_probe_1 = (math.sin(final_angle)) ** 2
        prob_probe_0 = (math.cos(final_angle)) ** 2
        
        live_predictions = prob_probe_1  # Incorrectly say it's live
        dud_predictions = prob_probe_0  # Correctly say it's dud
        detonations = 0.0
    
    return {
        'live_predictions': live_predictions,
        'dud_predictions': dud_predictions,
        'detonations': detonations
    }
