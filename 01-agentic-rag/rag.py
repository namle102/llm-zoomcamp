INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()

class RAGBase:
    def __init__(
        self,
        index,
        llm,
        prompt_template=PROMPT_TEMPLATE,
        instructions=INSTRUCTIONS,
        course='llm-zoomcamp',
        model='gpt-5.4-mini'
    ):
        self.index = index
        self.llm = llm
        self.prompt_template = prompt_template
        self.instructions = instructions
        self.course = course
        self.model = model

    def search(self, query, num_results=5):
        boost_dict = {'question': 3.0, 'section': 0.5}
        filter_dict = {'course': self.course}
        return self.index.search(
            query,
            num_results=num_results,
            boost_dict=boost_dict,
            filter_dict=filter_dict
        )
    
    def build_context(self, search_results):
        lines = []
        for doc in search_results:
            lines.append('S: ' + doc['section'])
            lines.append('Q: ' + doc['question'])
            lines.append('A: ' + doc['answer'])
            lines.append('')
        return "\n".join(lines).strip()
    
    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        prompt = self.prompt_template.format(
            question=query,
            context=context
        )
        return prompt
    
    def call_llm(self, prompt):
        input_message = [
            {
                "role": "system",
                "content": self.instructions
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        res = self.llm.responses.create(
            model=self.model,
            input=input_message
        )
        return res.output_text
    
    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.call_llm(prompt)
        return answer