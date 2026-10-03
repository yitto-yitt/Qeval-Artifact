# EVAL_META: task_id=40, framework=cirq, class=1
import cirq

def init_random_3qubit(desired_vector):
    q = cirq.LineQubit.range(3)
    q2, q1, q0 = q[2], q[1], q[0]
    circuit = cirq.Circuit()
    circuit.append(cirq.StatePreparationChannel(desired_vector).on(q2, q1, q0))
    circuit.append(cirq.measure(q2, q1, q0, key='m'))
    simulator = cirq.Simulator(seed=42)
    result = simulator.run(circuit, repetitions=1024)
    hist = result.histogram(key='m')
    total = sum(hist.values())
    return {format(k, '03b'): v / total for k, v in hist.items()}
