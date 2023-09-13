def pagination(page:int , page_size: int, output: list):
    """
    Args:
        output: complete output produced by the function ready to be paginated

    Returns:
        list : paginated results based on the arguments
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_results = output[start_index:end_index]
    return paginated_results



def calculate_similarity_score(response1, response2):
    """
    Function to calculate similarity score between two sets of responses.

    Args:
        response1 : List of responses for the first candidate.
        response2 : List of responses for the second candidate.

    Returns:
        string: Similarity score (% of matching answers).
    """
    if len(response1) != len(response2):
        raise ValueError("Response lengths do not match")

    # similarity_score = sum(1 for a, b in zip(response1, response2) if a == b)


    similarity_score = 0
    total = 20

    for (a, b) in zip(response1, response2):
        if a is None or b is None: # leave the none values
            total = total-1
        else:
            if a == b:
                similarity_score += 1

    if total == 0:
        return "0%" # there is no similarity 
        #(for the case when first half given by candidate 1 is None and second half given by candidate 2 is None)

    percentage = similarity_score / total * 100
    formatted_percentage = f"{percentage:.2f}%"
    return formatted_percentage