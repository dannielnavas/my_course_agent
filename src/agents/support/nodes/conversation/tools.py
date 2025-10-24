openai_vector_store_ids = [
    "vs_68fa19c8385881918734a172b75bd5ff"
]

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": openai_vector_store_ids,
}

tools = [file_search_tool]
