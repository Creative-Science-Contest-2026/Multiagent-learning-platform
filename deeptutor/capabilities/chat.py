"""Agentic chat capability."""

from __future__ import annotations

from deeptutor.core.capability_protocol import BaseCapability, CapabilityManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus
from deeptutor.agents.chat.agentic_pipeline import CHAT_OPTIONAL_TOOLS, AgenticChatPipeline
from deeptutor.capabilities.request_contracts import get_capability_request_schema
from deeptutor.services.runtime_policy import ensure_runtime_policy, format_chat_system_context


class ChatCapability(BaseCapability):
    manifest = CapabilityManifest(
        name="chat",
        description="Agentic chat with autonomous tool selection across enabled tools.",
        stages=["thinking", "acting", "observing", "responding"],
        tools_used=CHAT_OPTIONAL_TOOLS,
        cli_aliases=["chat"],
        request_schema=get_capability_request_schema("chat"),
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        policy = ensure_runtime_policy(context, self.name)
        policy_system_context = format_chat_system_context(policy)
        if policy_system_context:
            if context.memory_context.strip():
                context.memory_context = f"{policy_system_context}\n\n{context.memory_context}"
            else:
                context.memory_context = policy_system_context
        await stream.progress(
            message="Runtime policy slices assembled.",
            source=self.name,
            stage="thinking",
            metadata=context.metadata.get("runtime_policy", {}).get("debug", {}),
        )
        pipeline = AgenticChatPipeline(language=context.language)
        await pipeline.run(context, stream)
