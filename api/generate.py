import search

DOC_LIMITS = 20
THRESHOLD = 0.25
MAX_LENGTH = 6000


def generate_prompt(query: str) -> str:
    recommendations = search.find_best_documents(
        query, documents=search.documents, count=DOC_LIMITS
    )
    recommendations = [r for r in recommendations if r["distance"] < THRESHOLD]

    prompt = ""
    for doc in recommendations:
        raw_doc = search.data.iloc[doc["index"]]

        prompt += f"/* Write SQL query: {raw_doc['name']} */\n"
        prompt += raw_doc["query"].strip()
        prompt += "\n\n"

        if len(prompt) >= MAX_LENGTH:
            break

    prompt += f"/* Write SQL query: {query} */\n"
    return prompt


def generate_sql(query: str) -> dict:
    prompt = generate_prompt(query)
    result = search.openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=512,
        temperature=0,
        stop=["STOP", "/* Write SQL"],
    )

    return {"sql": result.choices[0].text.strip()}
