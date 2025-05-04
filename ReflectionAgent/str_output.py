from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-1.5-pro')

class Country(BaseModel):
    name: str = Field(description="Name of the country")
    capital: str = Field(description="Capital of the country")
    languages: List[str] = Field(description="Languages spoken in the country")


structured_llm = llm.with_structured_output(Country)
structured_response = structured_llm.invoke(
    "What is the capital of France? What languages are spoken in France?"
)
print(structured_response.name)





# from typing_extensions import Annotated, TypedDict
# from typing import Optional


# # TypedDict
# class Joke(TypedDict):
#     """Joke to tell user."""

#     setup: Annotated[str, ..., "The setup of the joke"]

#     # Alternatively, we could have specified setup as:

#     # setup: str                    # no default, no description
#     # setup: Annotated[str, ...]    # no default, no description
#     # setup: Annotated[str, "foo"]  # default, no description

#     punchline: Annotated[str, ..., "The punchline of the joke"]
#     rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


# structured_llm = llm.with_structured_output(Joke)

# structured_llm.invoke("Tell me a joke about cats")