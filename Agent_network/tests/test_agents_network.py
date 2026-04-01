import pytest
from structs import Agent, HEXACOProfile, PostSignals, Post
from network import build_network, NetworkConfig, assign_clusters
from prompts import compute_action_probabilities, describe_trait

# --- 1. HEXACO 分布测试 ---
def test_hexaco_distribution_range():
    """验证 HEXACO 随机数值是否在 [0, 1] 范围内"""
    profile = HEXACOProfile.random()
    traits = [profile.honesty_humility, profile.emotionality, profile.extraversion, 
              profile.agreeableness, profile.conscientiousness, profile.openness]
    for val in traits:
        assert 0.0 <= val <= 1.0

# --- 2. 交互规则逻辑测试 ---
def test_action_probability_normalization():
    """验证动作概率计算逻辑"""
    profile = HEXACOProfile.random()
    signals = PostSignals(0.5, 0.5, 0.5, 0.5, "source_1", 1)
    
    probs = compute_action_probabilities(profile, signals)
    
    # 验证关键行为概率是否存在且为正数
    assert "like" in probs
    assert "retweet" in probs
    assert probs["like"] >= 0
    # 验证互动概率总和（互动率 + 忽略率）的逻辑一致性
    total_engagement = sum(v for k, v in probs.items() if k != "ignore")
    # 根据代码逻辑，engagement 概率应该等于 profile.extraversion 经修正后的值
    assert total_engagement <= 1.0

def test_trait_description_mapping():
    """验证性格得分对应的文本描述是否准确"""
    # 测试边界值：1.0 应该对应最高等级的描述
    high_desc = describe_trait("honesty_humility", 1.0)
    assert "strict standard of accuracy" in high_desc
    # 测试低分描述
    low_desc = describe_trait("honesty_humility", 0.1)
    assert "deliberately distort" in low_desc

# --- 3. 网络拓扑与节点生成测试 ---
def test_network_node_creation():
    """验证网络是否正确生成了对应数量的c节点"""
    agents = [Agent(id=i, name=f"Agent_{i}", profile=HEXACOProfile.random()) for i in range(20)]
    config = NetworkConfig(agents_per_cluster=10)
    
    social_net = build_network(agents, config)
    
    # 验证节点总数
    assert social_net.graph.number_of_nodes() == 20
    # 验证集群数量：20个agent，每10个一簇，应有2个簇
    assert len(social_net.clusters) == 2

def test_cluster_hub_logic():
    """验证外向度最高的 Agent 是否被选为 Hub"""
    a1 = Agent(1, "Quiet", HEXACOProfile(0.5, 0.5, 0.1, 0.5, 0.5, 0.5))
    a2 = Agent(2, "Loud", HEXACOProfile(0.5, 0.5, 0.9, 0.5, 0.5, 0.5)) # 高外向度
    
    # 强制他们在同一个集群
    from network import get_cluster_hub
    hub = get_cluster_hub([a1, a2])
    
    assert hub.id == 2
    assert hub.name == "Loud"