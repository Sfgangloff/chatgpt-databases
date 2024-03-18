from pydantic import BaseModel, Field

class Subsection(BaseModel):
    number: int = Field(description="the number of the subsection within the section it is contained in.")
    title: str = Field(description="the title of the subsection.")

class Section(BaseModel):
    number: int = Field()
    title: str = Field(description="the title of the section.")
    subsections: list[Subsection] = Field(description='A list of subsections in a section.')

class Document(BaseModel):
    sections: list[Section] = Field(description='A document, which consists in a list of sections.')

class IndexElement(BaseModel):
    word: str = Field(description='A word inside an index.')

class Index(BaseModel):
    words: list[IndexElement] = Field(description='An index, which consists in a list of technical words which are contained in a technical text.')
    