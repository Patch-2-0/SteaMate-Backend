# from agents import Agent, Runner
# from vectorstore import create_search_tool
# from utils_v5 import game_info_search
# from config.settings import OPENAI_API_KEY

# # 벡터스토어 검색 도구 생성
# file_search_tool = create_search_tool()

# # 에이전트 생성
# game_agent = Agent(
#     name="GameSearchAgent",
#     instructions="You are a game assistant. You can search for games in the vector store.",
#     tools=[file_search_tool, game_info_search]
# )

# # 스트리밍 실행
# async def stream_game_search(query):
#     result = await Runner.run(game_agent, query, stream=True)
#     return result

# # 에이전트를 스트리밍 모드로 실행하는 함수
# async def run_game_agent_with_streaming(query):
#     stream = await game_agent.arun(query, stream=True)
    
#     # 스트리밍 응답 처리
#     async for chunk in stream:
#         if chunk.delta:  # 새로운 텍스트 청크가 있는 경우
#             yield chunk.delta  # 또는 필요한 처리 수행
#         elif chunk.tool_calls:  # 도구 호출이 있는 경우
#             # 도구 호출 처리
#             pass
        
#     # 최종 결과 반환
#     return stream.final_output 

