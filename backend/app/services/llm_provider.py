"""LLM Provider interface and implementations"""

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    @abstractmethod
    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs,
    ) -> str:
        """Generate a completion from the LLM"""
        pass

    @abstractmethod
    def generate_structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate structured output matching a schema"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None

    def _get_client(self):
        """Lazy initialization of OpenAI client"""
        if self._client is None:
            try:
                import openai

                self._client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "OpenAI package not installed. Install with: pip install openai"
                )
        return self._client

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs,
    ) -> str:
        """Generate a completion from OpenAI"""
        client = self._get_client()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        return response.choices[0].message.content

    def generate_structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate structured output using OpenAI function calling"""
        client = self._get_client()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            **kwargs,
        )

        content = response.choices[0].message.content
        return json.loads(content)

    def is_available(self) -> bool:
        """Check if OpenAI is available"""
        return self.api_key is not None


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None

    def _get_client(self):
        """Lazy initialization of Anthropic client"""
        if self._client is None:
            try:
                import anthropic

                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "Anthropic package not installed. Install with: pip install anthropic"
                )
        return self._client

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs,
    ) -> str:
        """Generate a completion from Anthropic"""
        client = self._get_client()

        response = client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

        return response.content[0].text

    def generate_structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate structured output from Anthropic"""
        client = self._get_client()

        enhanced_prompt = f"{prompt}\n\nRespond with valid JSON matching this schema: {json.dumps(schema)}"

        response = client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=system_prompt or "",
            messages=[{"role": "user", "content": enhanced_prompt}],
            **kwargs,
        )

        content = response.content[0].text
        return json.loads(content)

    def is_available(self) -> bool:
        """Check if Anthropic is available"""
        return self.api_key is not None


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing and development"""

    def __init__(self, model: Optional[str] = None, **_ignored: Any):
        self.model = model or "mock-model"

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        **kwargs,
    ) -> str:
        """Generate a mock completion"""
        return f"Mock LLM response for: {prompt[:50]}..."

    def generate_structured_output(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate mock structured output"""
        return {
            "mock": True,
            "prompt": prompt[:50],
            "schema": schema,
        }

    def is_available(self) -> bool:
        """Mock provider is always available"""
        return True


class LLMProviderFactory:
    """Factory for creating LLM providers"""

    _providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "mock": MockLLMProvider,
    }

    @classmethod
    def create(
        cls, provider_name: str, model: Optional[str] = None, **kwargs
    ) -> LLMProvider:
        """Create an LLM provider by name"""
        if provider_name not in cls._providers:
            raise ValueError(
                f"Unknown provider: {provider_name}. Available: {list(cls._providers.keys())}"
            )

        provider_class = cls._providers[provider_name]
        if model:
            return provider_class(model=model, **kwargs)
        return provider_class(**kwargs)

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """Register a new provider"""
        cls._providers[name] = provider_class

    @classmethod
    def list_providers(cls) -> List[str]:
        """List available providers"""
        return list(cls._providers.keys())
