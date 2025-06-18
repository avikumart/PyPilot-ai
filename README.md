
![pypilot_github-banner](https://github.com/user-attachments/assets/98829416-ba33-4813-bff7-36c6b84ca0dc)


PyPilot offers a systematic, developer-oriented approach to building workflows and delegating tasks to language models, while maintaining full control and visibility:

- Design focused, trackable [tasks](https://pypilot.ai/concepts/tasks) for AI execution.
- Deploy specialized AI [agents](https://pypilot.ai/concepts/agents) tailored to specific tasks.
- Link tasks into cohesive [flows](https://pypilot.ai/concepts/flows) for sophisticated orchestration.

## Quick Start

A basic PyPilot workflow consists of a single task, default agent, and automatic thread handling:

```python
import pypilot as cf

result = pypilot.run("Write a short poem about artificial intelligence")

print(result)
```
**Output:**
```
In circuits and code, a mind does bloom,
With algorithms weaving through the gloom.
A spark of thought in silicon's embrace,
Artificial intelligence finds its place.
```

## Why Choose PyPilot?

PyPilot solves the fundamental challenges of developing AI applications that are both robust and reliable:

- 🧩 [**Task-First Design**](https://pypilot.ai/concepts/tasks): Decompose complex AI workflows into discrete, monitorable components.
- 🔒 [**Structured Outputs**](https://pypilot.ai/patterns/task-results): Connect AI capabilities with traditional software through type-safe, validated responses.
- 🤖 [**Purpose-Built Agents**](https://pypilot.ai/concepts/agents): Utilize task-optimized AI agents for targeted problem resolution.
- 🎛️ [**Adaptive Control**](https://pypilot.ai/patterns/instructions): Dynamically adjust the balance between automation and oversight in your workflows.
- 🕹️ [**Multi-Agent Coordination**](https://pypilot.ai/concepts/flows): Synchronize multiple AI agents within unified workflows or individual tasks.
- 🔍 [**Built-in Monitoring**](https://github.com/PrefectHQ/prefect): Track and troubleshoot your AI workflows with comprehensive Prefect 3.0 integration.
- 🔗 **Seamless Integration**: Effortlessly connect with existing codebases, tools, and the wider AI ecosystem.

## Getting Started

Install PyPilot using `pip`:

```bash
pip install pypilot
```

Then set up your LLM provider. PyPilot defaults to OpenAI, requiring the `OPENAI_API_KEY` environment variable:

```
export OPENAI_API_KEY=your-api-key
```

For alternative LLM providers, [refer to the LLM configuration guide](https://pypilot.ai/guides/configure-llms).

## Advanced Workflow Example

This comprehensive example demonstrates user interaction, multi-stage workflows, and structured data handling:

```python
import pypilot as cf
from pydantic import BaseModel


class ResearchProposal(BaseModel):
    title: str
    abstract: str
    key_points: list[str]


@cf.flow
def research_proposal_flow():

    # Task 1: Get the research topic from the user
    user_input = cf.Task(
        "Work with the user to choose a research topic",
        interactive=True,
    )
    
    # Task 2: Generate a structured research proposal
    proposal = cf.run(
        "Generate a structured research proposal",
        result_type=ResearchProposal,
        depends_on=[user_input]
    )
    
    return proposal


result = research_proposal_flow()

print(result.model_dump_json(indent=2))
```
<details>
<summary><i>Click to see results</i></summary>
</br>

>**Conversation:**
> ```text
> Agent: Hello! I'm here to help you choose a research topic. Do you have 
> any particular area of interest or field you would like to explore? 
> If you have any specific ideas or requirements, please share them as well.
> 
> User: Yes, I'm interested in LLM agentic workflows
> ```
> 
> **Proposal:**
> ```json
> {
>     "title": "AI Agentic Workflows: Enhancing Efficiency and Automation",
>     "abstract": "This research proposal aims to explore the development and implementation of AI agentic workflows to enhance efficiency and automation in various domains. AI agents, equipped with advanced capabilities, can perform complex tasks, make decisions, and interact with other agents or humans to achieve specific goals. This research will investigate the underlying technologies, methodologies, and applications of AI agentic workflows, evaluate their effectiveness, and propose improvements to optimize their performance.",
>     "key_points": [
>         "Introduction: Definition and significance of AI agentic workflows, Historical context and evolution of AI in workflows",
>         "Technological Foundations: AI technologies enabling agentic workflows (e.g., machine learning, natural language processing), Software and hardware requirements for implementing AI workflows",
>         "Methodologies: Design principles for creating effective AI agents, Workflow orchestration and management techniques, Interaction protocols between AI agents and human operators",
>         "Applications: Case studies of AI agentic workflows in various industries (e.g., healthcare, finance, manufacturing), Benefits and challenges observed in real-world implementations",
>         "Evaluation and Metrics: Criteria for assessing the performance of AI agentic workflows, Metrics for measuring efficiency, accuracy, and user satisfaction",
>         "Proposed Improvements: Innovations to enhance the capabilities of AI agents, Strategies for addressing limitations and overcoming challenges",
>         "Conclusion: Summary of key findings, Future research directions and potential impact on industry and society"
>     ]
> }
> ```
</details>

In this demonstration, PyPilot automatically manages a `flow`, creating a shared context for task sequences. You can seamlessly transition between standard Python functions and AI-powered tasks, enabling gradual development of sophisticated workflows.

## Explore Further

To learn more about PyPilot:

- [Browse the complete documentation](https://pypilot.ai)
- [Discover sample projects](https://pypilot.ai/examples)
