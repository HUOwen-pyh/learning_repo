"""第11晚：三个 NP 关系的独立证书验证器。"""

def verify_hamiltonian_path(graph, certificate):
    vertices = set(graph)
    if len(certificate) != len(vertices) or set(certificate) != vertices:
        return False
    return all(v in graph[u] for u, v in zip(certificate, certificate[1:]))

def verify_clique(graph, certificate, k):
    chosen = list(certificate)
    if len(chosen) != k or len(set(chosen)) != k:
        return False
    return all(v in graph[u] for i, u in enumerate(chosen) for v in chosen[i+1:])

def verify_subset_sum(numbers, target, certificate):
    indices = list(certificate)
    return (len(indices) == len(set(indices))
            and all(0 <= i < len(numbers) for i in indices)
            and sum(numbers[i] for i in indices) == target)

if __name__ == "__main__":
    graph = {
        0:{1,2}, 1:{0,2,3}, 2:{0,1,3}, 3:{1,2}
    }
    assert verify_hamiltonian_path(graph, [0,1,2,3])
    assert not verify_hamiltonian_path(graph, [0,1,3,3])
    assert verify_clique(graph, [0,1,2], 3)
    assert not verify_clique(graph, [0,1,3], 3)
    nums = [3,7,11,15]
    assert verify_subset_sum(nums, 18, [1,2])
    assert not verify_subset_sum(nums, 18, [0,3,3])
    print("Valid certificates passed; malformed and false certificates were rejected.")
    # 动手改造：为图着色写 verifier；确认它只检查证书而不搜索颜色。
