import unittest
from typing import Dict
from pipeline import Pipeline, PipelineList, Hook, PipelineRegistry, HookRegistry


# 호출 여부를 확인하기 위한 SampleHook 클래스
@HookRegistry.register
class SampleHook(Hook):
    def __init__(self, memory, **kwargs):
        super().__init__(**kwargs)
        self.memory = memory  # 호출 횟수 기록

    def forward(self, **kwargs) -> None:
        self.memory[0] += 1  # 호출될 때마다 증가


# 파이프라인 클래스
@PipelineRegistry.register
class SamplePipeline(Pipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def forward(self, **kwargs) -> Dict:
        return kwargs


class TestPipeline(unittest.TestCase):
    def test_sample_pipeline(self):
        memory = [0]
        cfg = {
            "name": "PipelineList",
            "pipeline": [
                {
                    "name": "SamplePipeline",
                    "forward_pre_hook": [{"name": "SampleHook", "memory": memory}],
                    "forward_post_hook": [{"name": "SampleHook", "memory": memory}],
                }
            ],
        }

        # 파이프라인 빌드
        pipeline = PipelineRegistry.build(**cfg)

        # 파이프라인 실행
        result = pipeline(data=42)

        # 결과 검증
        self.assertEqual(result["data"], 42)

        # SampleHook이 몇번 호출 되었는지 검증
        self.assertEqual(memory[0], 2)


if __name__ == "__main__":
    unittest.main()
