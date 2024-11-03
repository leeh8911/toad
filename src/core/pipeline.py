import abc
from typing import Any, List, Dict

from registry import REGISTRY_FACTORY

PipelineRegistry = REGISTRY_FACTORY("PipelineRegistry")
HookRegistry = REGISTRY_FACTORY("HookRegistry")


class Hook(metaclass=abc.ABCMeta):
    """
    Abstract base class for hooks used in the pipeline.
    Hooks perform inspections, logging, or other operations
    on input arguments without modifying the output.
    """

    def __init__(self, name: str = None, parent=None, **kwargs):
        self._name = name if name else self.__class__.__name__
        self_parent = parent

    @property
    def name(self) -> str:
        return self._name

    @abc.abstractmethod
    def forward(self, **kwargs) -> None:
        """
        Perform an action on the input arguments.

        Args:
            **kwargs: Input arguments passed to the hook.
        """
        pass

    def __call__(self, **kwargs) -> None:

        self.forward(**kwargs)


class Pipeline(metaclass=abc.ABCMeta):
    """
    Abstract base class for a pipeline step.
    Each step includes optional pre- and post-processing hooks,
    along with a forward method to process data.

    Attributes:
        name (str): Name of the pipeline step.
        prev (Pipeline): Reference to the previous pipeline step.
        post (Pipeline): Reference to the next pipeline step.
    """

    def __init__(self, name: str = None, **kwargs):
        forward_pre_hook_cfg_list = kwargs.get("forward_pre_hook", [])
        forward_post_hook_cfg_list = kwargs.get("forward_post_hook", [])
        self._forward_pre_hook_list: List[Hook] = [
            HookRegistry.build(**cfg, parent=self) for cfg in forward_pre_hook_cfg_list
        ]
        self._forward_post_hook_list: List[Hook] = [
            HookRegistry.build(**cfg, parent=self) for cfg in forward_post_hook_cfg_list
        ]

        self._name = name if name else self.__class__.__name__
        self._prev = None
        self._post = None

    @property
    def name(self) -> str:
        """Returns the name of the pipeline step."""
        return self._name

    @property
    def prev(self) -> "Pipeline":
        """Returns the previous pipeline step."""
        return self._prev

    @prev.setter
    def prev(self, prev: "Pipeline") -> None:
        self._prev = prev

    @property
    def post(self) -> "Pipeline":
        """Returns the next pipeline step."""
        return self._post

    @post.setter
    def post(self, post: "Pipeline") -> None:
        self._post = post

    @abc.abstractmethod
    def forward(self, **kwargs) -> Dict:
        """
        Defines the processing logic of the pipeline step.

        Args:
            **kwargs: Input arguments for processing.

        Returns:
            Dict: The result of processing.
        """
        pass

    def __call__(self, **kwargs) -> Dict:
        """
        Executes the pipeline step with pre- and post-hooks.

        Args:
            **kwargs: Input arguments for processing.

        Returns:
            Dict: Result after processing by the forward method.
        """
        for hook in self._forward_pre_hook_list:
            hook(**kwargs)  # Pre-hooks

        result = self.forward(**kwargs)  # Main processing

        for hook in self._forward_post_hook_list:
            hook(**kwargs)  # Post-hooks

        return result


@PipelineRegistry.register
class PipelineList(Pipeline):
    """
    A sequence of pipeline steps executed in order.

    Attributes:
        pipeline (List[Pipeline]): List of pipeline steps.
    """

    def __init__(self, **kwargs):
        assert "pipeline" in kwargs, "pipeline key must be provided in kwargs"
        super().__init__(name="PipelineList")

        self.pipeline: List[Pipeline] = []
        prev_pipe = None
        for pipe_cfg in kwargs["pipeline"]:
            pipe = PipelineRegistry.build(**pipe_cfg)
            self.pipeline.append(pipe)
            if prev_pipe:
                prev_pipe.post = pipe
                pipe.prev = prev_pipe
            prev_pipe = pipe

    def forward(self, **kwargs) -> Any:
        """
        Processes the input through each pipeline step in sequence.

        Args:
            **kwargs: Initial input for the pipeline.

        Returns:
            Any: Final output after processing through all steps.
        """
        result = kwargs
        for pipe in self.pipeline:
            result = pipe(**result if isinstance(result, dict) else {"data": result})
        return result

    def __call__(self, **kwargs) -> Any:
        """
        Calls the pipeline sequence.

        Args:
            **kwargs: Initial input for the pipeline.

        Returns:
            Any: Final output after processing through all steps.
        """
        return self.forward(**kwargs)
