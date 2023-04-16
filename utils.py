import re, os, requests, isodate
# import dotenv

# dotenv.load_dotenv(".env")
API = os.getenv("KEY")

BASE_URL = "https://www.googleapis.com/youtube/v3"
URL1 = "{}/playlistItems?part=contentDetails&maxResults=50&fields=items/contentDetails/videoId,nextPageToken&key={}&playlistId={}&pageToken="
URL2 = (
    "{}/videos?&part=contentDetails&id={}&key={}&fields=items/contentDetails/duration"
)

# https://www.youtube.com/watch?v=aqvDTCpNRek&list=PLu0W_9lII9agICnT8t4iYVSZ3eykIAOME

id_regex = re.compile("^([\S]+list=)?([\w_-]+)[\S]*$")

DISPLAY_TEXT = """
No of videos : {}

Average length of video : {}

Total length of playlist : {}

At 1.25x : {}

At 1.50x : {}

At 1.75x : {}

At 2.00x : {}
"""


def get_id(url):
    return id_regex.match(url).group(2)


def get_time_in_days(seconds):
    days = divmod(seconds, 86400)
    hours = divmod(days[1], 3600)
    minutes = divmod(hours[1], 60)
    seconds = divmod(minutes[1], 60)
    final_time = ""
    if days[0] > 0:
        final_time += f"{days[0]} day "
    if hours[0] > 0:
        final_time += f"{hours[0]} hours "
    if minutes[0] > 0:
        final_time += f"{minutes[0]} minutes "
    if seconds[0] > 0:
        final_time += f"{seconds[0]} seconds "

    return final_time


def get_time(videos):
    seconds = 0
    for video in videos:
        seconds += video.seconds

    average_length = seconds / len(videos)
    total_length = seconds
    at_1_25 = seconds / 1.25
    at_1_50 = seconds / 1.50
    at_1_75 = seconds / 1.75
    at_2_00 = seconds / 2.00

    return (
        get_time_in_days(average_length),
        get_time_in_days(total_length),
        get_time_in_days(at_1_25),
        get_time_in_days(at_1_50),
        get_time_in_days(at_1_75),
        get_time_in_days(at_2_00),
    )


def get_data(id):
    try:
        next_page = ""
        duration = []

        while True:
            vid_ids = []
            results = requests.get(URL1.format(BASE_URL, API, id) + next_page).json()
            for item in results["items"]:
                vid_ids.append(item["contentDetails"]["videoId"])

            details = requests.get(URL2.format(BASE_URL, ",".join(vid_ids), API)).json()
            for item in details.get("items", []):
                duration.append(
                    isodate.parse_duration(item["contentDetails"]["duration"])
                )
            if "nextPageToken" in results and len(vid_ids) < 500:
                next_page = results["nextPageToken"]
            else:
                break

        average_length, total_length, at_1_25, at_1_50, at_1_75, at_2_00 = get_time(
            duration
        )
        # return DISPLAY_TEXT.format(no_of_video,average_length,total_length,at_1_25,at_1_50,at_1_75,at_2_00)
        return DISPLAY_TEXT.format(
            len(duration),
            average_length,
            total_length,
            at_1_25,
            at_1_50,
            at_1_75,
            at_2_00,
        )
    except Exception as e:
        return f"Encountered Error: {e} => {results['error']['message']}\nKindly raise an issue on github with error"
