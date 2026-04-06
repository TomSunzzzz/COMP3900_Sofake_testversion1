import sys
import os
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
agent_network_path = os.path.join(parent_dir, "Agent_network")

if agent_network_path not in sys.path:
    sys.path.insert(0, agent_network_path)

from structs import Agent, HEXACOProfile, PostSignals, Post
from network import build_network, NetworkConfig, assign_clusters
from prompts import compute_action_probabilities, describe_trait
# --- 1. HEXACO Distribution Tests ---
def test_hexaco_distribution_range():
    """Verify that HEXACO random values are within the [0.0, 1.0] range."""
    profile = HEXACOProfile.random()
    traits = [profile.honesty_humility, profile.emotionality, profile.extraversion, 
              profile.agreeableness, profile.conscientiousness, profile.openness]
    for val in traits:
        assert 0.0 <= val <= 1.0

# --- 2. Interaction Logic Tests ---
def test_action_probability_normalization():
    """Verify the calculation logic for action probabilities."""
    profile = HEXACOProfile.random()
    signals = PostSignals(0.5, 0.5, 0.5, 0.5, "source_1", 1)
    
    probs = compute_action_probabilities(profile, signals)
    
    # Ensure key behavior probabilities exist and are non-negative
    assert "like" in probs
    assert "retweet" in probs
    assert probs["like"] >= 0
    
    # Verify logical consistency of total engagement (interaction + ignore)
    total_engagement = sum(v for k, v in probs.items() if k != "ignore")
    
    # Based on the implementation, total engagement should not exceed 1.0
    assert total_engagement <= 1.0

def test_trait_description_mapping():
    """Verify that trait scores are accurately mapped to text descriptions."""
    # Boundary test: 1.0 should map to the highest standard description
    high_desc = describe_trait("honesty_humility", 1.0)
    assert "strict standard of accuracy" in high_desc
    
    # Low score test: Verify description for low trait values
    low_desc = describe_trait("honesty_humility", 0.1)
    assert "deliberately distort" in low_desc

# --- 3. Network Topology & Node Generation Tests ---
def test_network_node_creation():
    """Verify that the network generates the correct number of nodes and clusters."""
    agents = [Agent(id=i, name=f"Agent_{i}", profile=HEXACOProfile.random()) for i in range(20)]
    config = NetworkConfig(agents_per_cluster=10)
    
    social_net = build_network(agents, config)
    
    # Verify total node count in the graph
    assert social_net.graph.number_of_nodes() == 20
    
    # Verify cluster count: 20 agents at 10 per cluster should yield exactly 2 clusters
    assert len(social_net.clusters) == 2

def test_cluster_hub_logic():
    """Verify that the Agent with the highest extraversion is selected as the Hub."""
    a1 = Agent(1, "Quiet", HEXACOProfile(0.5, 0.5, 0.1, 0.5, 0.5, 0.5))
    a2 = Agent(2, "Loud", HEXACOProfile(0.5, 0.5, 0.9, 0.5, 0.5, 0.5)) # High extraversion
    
    # Internal function test for Hub selection
    from Agent_network.network import get_cluster_hub
    hub = get_cluster_hub([a1, a2])
    
    assert hub.id == 2
    assert hub.name == "Loud"