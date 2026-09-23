import pytest
from app.federated.aggregation_server import federated_aggregation_server

def test_federated_averaging_aggregation_with_differential_privacy():
    client_updates = [
        {"clientId": "client_1", "gradientWeights": [0.12, 0.45, -0.08]},
        {"clientId": "client_2", "gradientWeights": [0.18, 0.35, -0.02]},
        {"clientId": "client_3", "gradientWeights": [0.15, 0.40, -0.05]}
    ]

    agg_res = federated_aggregation_server.aggregate_client_gradients(client_updates)

    assert agg_res["aggregation_algorithm"] == "FEDERATED_AVERAGING_FEDAVG"
    assert agg_res["num_clients_aggregated"] == 3
    assert agg_res["differential_privacy_verified"] is True
    assert len(agg_res["global_model_weights"]) == 3
    assert agg_res["global_model_weights"][0] == 0.15 # (0.12 + 0.18 + 0.15) / 3
