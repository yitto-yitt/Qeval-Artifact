# EVAL_META: task_id=1, framework=cirq, class=1
import cirq
from cirq import Circuit, LineQubit
from cirq.sim import Simulator
import numpy as np

def run_bell_state_simulator():
    qubits = [LineQubit(i) for i in range(2)]
    bell = Circuit()
    bell.append(cirq.H(qubits[0]))
    bell.append(cirq.CNOT(qubits[0], qubits[1]))
    bell.append(cirq.measure(*qubits, key='meas'))
    
    simulator = Simulator()
    result = simulator.run(bell, repetitions=1000)
    measurements = result.measurements['meas']
    
    # Count occurrences of each bitstring
    counts = {}
    for meas in measurements:
        bitstring = ''.join(map(str, meas))
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
