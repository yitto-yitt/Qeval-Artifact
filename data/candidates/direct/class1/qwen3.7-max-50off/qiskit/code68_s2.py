# EVAL_META: task_id=68, framework=qiskit, class=1
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    """
    Zeno Elitzur-Vaidman bomb tester using 25 cycles.
    
    Uses the quantum Zeno effect to detect whether a bomb is live or a dud
    with high probability of correctly identifying a live bomb without detonating it.
    
    Each cycle applies a small Ry(pi/N) rotation. For a live bomb, mid-circuit
    measurements act as the bomb's photon detector. The Zeno effect suppresses
    transitions to the |1> state, keeping the photon in |0> with high probability.
    For a dud bomb, no measurement occurs and rotations accumulate to Ry(pi),
    flipping the qubit to |1>.
    """
    N = 25
    theta = np.pi / N
    shots = 100000

    if bomb_live:
        # Live bomb: the bomb acts as a measuring device each cycle.
        # If the qubit is |1>, the bomb detonates.
        # Mid-circuit measurements simulate the bomb's detector.
        qc = QuantumCircuit(1, N + 1)

        for i in range(N):
            qc.ry(theta, 0)
            qc.measure(0, i)  # Bomb "checks" the photon each cycle

        # Final measurement to determine prediction
        qc.measure(0, N)

        sim = AerSimulator()
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for bitstring, count in counts.items():
            bits = bitstring.replace(' ', '')
            # Qiskit bitstring order: c_N c_{N-1} ... c_1 c_0
            # bits[0] = c_N (final measurement)
            # bits[1:] = c_{N-1} ... c_0 (cycle measurements)
            final_bit = int(bits[0])
            cycle_bits = bits[1:]

            if '1' in cycle_bits:
                # Bomb detected photon in |1> at some cycle -> detonation
                detonations += count
            else:
                # Bomb never detected photon -> survived all cycles
                if final_bit == 0:
                    live_predictions += count
                else:
                    dud_predictions += count

        return {
            'live_predictions': live_predictions / shots,
            'dud_predictions': dud_predictions / shots,
            'detonations': detonations / shots
        }

    else:
        # Dud bomb: the detector is broken, no measurement occurs during cycles.
        # Rotations accumulate: N * Ry(pi/N) = Ry(pi), flipping |0> to |1>.
        qc = QuantumCircuit(1, 1)

        for i in range(N):
            qc.ry(theta, 0)

        qc.measure(0, 0)

        sim = AerSimulator()
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for bitstring, count in counts.items():
            bits = bitstring.replace(' ', '')
            final_bit = int(bits[0])

            if final_bit == 1:
                # Qubit flipped to |1> -> dud detected
                dud_predictions += count
            else:
                live_predictions += count

        return {
            'live_predictions': live_predictions / shots,
            'dud_predictions': dud_predictions / shots,
            'detonations': detonations / shots
        }

