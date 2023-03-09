Greetings reviewers!

Please review my Web application that parses data from the given URL or domain.

Technologies I've used:
`Python3.10`, `Flask`, `requests`, `BeautifulSoup`, `threading`, `SQLite3`

To run the application, you'll need to:

1. Clone the repo on your local machine;
2. Create virtualenv and activate it --> `source {env_folder}/bin/activate`;
3. Install required dependencies by running `pip install -r requirements.txt` command;
4. Run the Flask app by running `flask run` command in your terminal (make sure before running `flask run` to set
   the `FLASK_APP` env variable --> `export FLASK_APP=app/app.py`).

The Web application has two endpoints:

1. `/endpoint1` - gets `url` as an input, returns json response with the following body:
   `{
   "final_url": str,
   "final_satatus_code": int | None,
   "status_code": int,
   "title": str,
   "domain_name": str
   }`
2. `/endpoint2` - gets the `domain_name` as an input, returns json response with the following body:
   `{
   "active_page_count": int,
   "total_page_count": int,
   "url_list": list[str]
   }`
