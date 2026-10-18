from openai import OpenAI


client = OpenAI(
    # Ollama provides an OpenAI-compatible API at this local address.
    base_url="http://localhost:11434/v1",
    # Ollama does not require a real OpenAI API key, but the SDK requires a value.
    api_key="ollama",
)


def main():
    response = client.chat.completions.create(
        # Use a model tag installed in Ollama (check with `ollama list`).
        model="openllama",
        # Messages are sent in order; system sets behavior, user is the prompt.
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain Ollama in one sentence."},
        ],
        temperature=0.2,  # Randomness: 0 is more predictable; higher is more varied.
        max_tokens=128,  # Maximum generated tokens; supported by many Ollama versions.
        # Optional Chat Completions parameters. Uncomment only what you need.
        # Ollama implements only a subset of the OpenAI API; unsupported options
        # may be ignored or cause an error depending on your Ollama version.
        #
        # audio={"voice": "alloy", "format": "wav"},  # Request generated audio; generally hosted/API-specific.
        # frequency_penalty=0.0,  # Discourage words based on how often they already appeared.
        # function_call="none",  # Deprecated legacy function-calling control; prefer tool_choice.
        # functions=[{"name": "example", "parameters": {"type": "object", "properties": {}}}],  # Deprecated; prefer tools.
        # logit_bias={},  # Adjust token likelihoods by token ID; model/tokenizer-specific.
        # logprobs=True,  # Include token log probabilities in the response, if supported.
        # max_completion_tokens=128,  # Newer output-token limit; use instead of max_tokens when supported.
        # metadata={"purpose": "demo"},  # Attach metadata to a stored hosted-API response.
        # modalities=["text"],  # Choose output types, such as text or audio.
        # moderation=None,  # Provider-specific moderation options.
        # n=1,  # Number of completion choices to generate.
        # parallel_tool_calls=True,  # Allow multiple tool calls in one assistant turn.
        # prediction={"type": "content", "content": "expected text"},  # Supply expected output to speed up supported models.
        # presence_penalty=0.0,  # Discourage introducing topics already mentioned.
        # prompt_cache_key="demo",  # Cache-key hint for supported hosted providers.
        # prompt_cache_options=None,  # Provider-specific prompt-cache settings.
        # prompt_cache_retention="in_memory",  # Requested cache lifetime on supported hosted providers.
        # reasoning_effort="low",  # Reasoning budget for models that expose this control.
        # response_format={"type": "json_object"},  # Request JSON output, if the model supports it.
        # safety_identifier="local-demo-user",  # Privacy-safe identifier used by supported hosted providers.
        # seed=42,  # Best-effort repeatability; model output may still vary.
        # service_tier="default",  # Select a hosted service tier; not normally relevant to local Ollama.
        # stop=["END"],  # Stop generation when one of these strings is produced.
        # store=False,  # Request whether the provider stores this completion.
        # stream=True,  # Yield response chunks instead of one completed response.
        # stream_options={"include_usage": True},  # Add usage totals to a streaming response.
        # tool_choice="auto",  # Control whether and which tool the model may call.
        # tools=[  # Advertise functions the model may request the application to run.
        #     {
        #         "type": "function",
        #         "function": {
        #             "name": "get_weather",
        #             "description": "Get the weather for a city.",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {"city": {"type": "string"}},
        #                 "required": ["city"],
        #             },
        #         },
        #     }
        # ],
        # top_logprobs=2,  # Return this many likely alternatives per token; requires logprobs=True.
        # top_p=0.9,  # Nucleus sampling; considers tokens within this cumulative probability.
        # user="local-demo-user",  # Optional end-user identifier for supported hosted providers.
        # verbosity="low",  # Desired answer detail for models that support this control.
        # web_search_options={},  # Hosted web-search settings; not a local Ollama capability.
        #
        # Additional SDK/HTTP options (not model-generation settings):
        # extra_headers={"X-Example": "value"},  # Add HTTP headers to the request.
        # extra_query={"example": "value"},  # Add URL query-string parameters.
        # extra_body={"provider_option": "value"},  # Send provider-specific JSON fields.
        # timeout=30.0,  # Set the HTTP request timeout in seconds.
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
