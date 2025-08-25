Date: 250825

X-post via Reddit (/r/LocalLLama)

Hi everyone!
So, I have a bunch of models in ollama and it's mostly trial and error to see which one might work for a specific task (increasingly the factor I'm looking for is MCP/tool use).
I see value, however, in the diversity of options: certain models are undoubtedly better for code gen and others for text classification. But in most cases, I'd be happy for the selection logic to be done programatically. 
I use Open Router for cloud LLMs and was wondering if anyone had thought of some kind of middleware that might inject itself between Ollama API and act as a model selection rotuer - examining the user's request, parsing the model library, and then matching their workload with the best available model for the duration of that session.
Any recommendations much appreciated!
TIA!