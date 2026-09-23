import pytest
from app.quantum.qaoa_optimizer import qaoa_synastry_optimizer
from app.quantum.qmc_sampler import quantum_monte_carlo_sampler

def test_qaoa_ising_hamiltonian_formulation():
    scores = [{"P1": 0.85}, {"P2": 0.65}, {"P3": 0.72}]
    opt = qaoa_synastry_optimizer.optimize_group_confluence(scores, qaoa_depth_p=2)

    assert opt["num_qubits_evaluated"] == 3
    assert opt["convergence_status"] == "QUANTUM_GROUND_STATE_REACHED"
    assert 0.0 <= opt["qaoa_optimized_confluence_score"] <= 100.0

def test_quantum_monte_carlo_probability_sampling():
    res = quantum_monte_carlo_sampler.sample_365day_quantum_probability(base_probability=0.68, num_samples=1024)

    assert res["quantum_samples_evaluated"] == 1024
    assert res["classical_sample_count_equivalent"] == 1024 * 1024
    assert 0.0 <= res["quantum_sampled_probability"] <= 1.0
