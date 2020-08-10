# Trackrr.py (test.py)
# Trackkr.py Example

# Imports
import asyncio
from trackrr.client import Trackrr

# Create an async function
async def main():
    """ Searchs for a song using the Trackrr API """
    # This function returns more than 1 result
    # TODO: Return one result only, if possible

    # Specify the Trackrr client
    # You must specify an API key to this client
    client = Trackrr("API Key here")
    # Search Trackrr for a song based on a given query
    query = await client.search_song("Valentino")
    # Select the first result from the query
    # Print its contents (check the docs for other values)
    result = query[0]
    print(f"Song Name: {result.track_name}")
    print(f"Artists: {result.track_artists}")
    print(f"Song URL: {result.track_url}")
    # Close our Trackrr client
    # Always do this after each request
    await client.close()

# Run the function above (asynchronously)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
