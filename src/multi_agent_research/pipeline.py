from multi_agent_research.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

def run_research_pipeline(topic :str, on_step=None) -> dict:
    state = {}

    #search agent working
    print("\n"+" ="*50)
    print("Step 1 working")
    print("\n"+" ="*50)

    if on_step: on_step(1, "Search agent is finding sources")
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" :[("user" ,f"find recent and reliable and detailed information about : {topic}")]
    })

    state['search_results'] = search_result['messages'][-1].content

    print("\n search result",state['search_results'])


    #step 2
    print("\n"+" ="*50)
    print("Step 2 working - Reader Agent is scraping ")
    print("\n"+" ="*50)

    if on_step: on_step(2, "Reader agent is scraping the best source")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })


    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])


    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    if on_step: on_step(3, "Writer is drafting the report")
    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    if on_step: on_step(4, "Critic is reviewing the report")
    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)



