PROMPT_TEMPLATES = {

"table_of_contents" : {"template":"""What would be the table of contents of a book on "{subject}"? There should be around 10 sections and around 5 subsection per section (not including generic sections such as "References" or "Further reading").
                       
                       {format_instructions}""",
                       "input_keys":["subject","format_instructions"]},

"part_draft" : {"template":"""Write the part "{title}" of a book on "{subject}".""",
                "input_keys":["title","subject"]},

"index_draft" : {"template":"""You are writing a book on "{subject}". You have written the part whose title is "{title}" and the text is the following: "{text}".
                 Write an index for this part which contains only words which are contained in the text.""",
                 "input_keys":["subject","title","text"]},

"specific_index" : {"template":"""In the following list of words, which ones are technical and specific to "{title}": "{word_list}" ? Keep it as short as possible.
                    
                    {format_instructions}""",
                    "input_keys":["title","word_list"]},

"part" : {"template": """Write the part on "{title}" in a book about "{subject}".\n Write only the text and do not begin with "{title}". It should contain approximately 1250 words. \n Here is a list of terms that you can use for this purpose:{index}""",
          "input_keys":["title","subject","index"]},

"part_reduce" : {"template": """Remove the title part and intermediate sections titles from the following text:
                 
                 '{content}'.""",
          "input_keys":["content"]},

"distribute_index": {
                "template": """Match every word in the list "{word_list}" to a book part title in the following list: '{total_index}'.""",
                "input_keys":["word_list","total_index"]
}, 

"decompose_sections": {
    "template": """Break the subsection titled '{subsection_title}' in up to 5 subsubsections. This subsection is in a book on '{subject}' and in the section titled '{section_title}' whose subsections are: '{subsections_titles}'. Write the numbers of the subsubsections as integers (for instance 4 is valid but not 4.1 or 4.2). The titles of the subsubsections should not be a generic term like 'Subsection' or 'Concept'.
     
    {format_instructions}
    """
}

}
