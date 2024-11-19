import requests_with_caching 

# NOTE: the OMDb API uses http:// instead of https://
import json
# the movie data only 
def get_movie_data(name:str)->dict:
    query_dict = {'t': name, 'r': 'json'}
    request = requests_with_caching.get('http://www.omdbapi.com/', params=query_dict)
    response = json.loads(request.text)
    return response
#rating of the movie
def rt_rating(movie_data:dict)->int:
    rating = ""
    for rating_list in movie_data["Ratings"]:
        if rating_list["Source"]== "Rotten Tomatoes":
            rating = rating_list["Value"]
    if rating != "":
        int_rating = int(rating[:2])
    else: int_rating = -1
    return int_rating

# now dad jokes
def get_joke_data(one : str) -> dict:
    prm = {'term' : one , 'limit': 2}
    req = requests_with_caching.get('https://icanhazdadjoke.com/search' , params=prm)
    response = json.loads(req.text)
    return response

#Get Jokes for a Long Word from the Plot Description
def get_jokes(plot: str, verbosity=0) -> tuple[str, list[str]]:
    """
    Returns a tuple containing the longest word for which jokes were found
    and the jokes themselves. Break ties for longest word using the order in `plot`.
    Make sure that you strip punctuation from the word before you search for a joke.

    Parameters
    ----------
    plot : str
        The plot of a movie.

    verbosity : int (optional)
        If 0, no output is printed. If 1, some output is printed about which words were tried.
        Defaults to 0.

    Returns
    -------
    tuple[str, list[str]]
        A tuple containing the word that was used to search for a joke and a list of two joke strings.
    """
    import string

    # Step 1: Remove punctuation and split words
    words = plot.translate(str.maketrans("", "", string.punctuation)).split()

    # Step 2: Sort words by length (longest to shortest) and by order of appearance for ties
    words.sort(key=lambda w: (-len(w), plot.index(w)))

    # Step 3: Iterate through sorted words and find jokes
    for word in words:
        if verbosity == 1:
            print(f"Trying word: {word}")

        # Fetch jokes for the current word
        joke_data = get_joke_data(word)
        
        # If jokes are found, return the word and the list of jokes
        if joke_data['results']:
            jokes = [result['joke'] for result in joke_data['results']]
            return (word, jokes)

    # Step 4: If no jokes are found, return (None, None)
    return (None, None)
