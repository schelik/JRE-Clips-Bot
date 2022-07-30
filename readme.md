# JRE-Clips-Bot
<p>Just provide a YouTube video link with a timestamp in the description. The bot downloads the video, cuts it into clips, and creates thumbnails for the clips. It then uploads the JRE-style clips to your YouTube channel.</p>

[![Demo Video](https://img.youtube.com/vi/H2r7QgZQmu4/0.jpg)](https://www.youtube.com/watch?v=H2r7QgZQmu4)
<p>Languages/Libraries: Python, Pillow, Pytube, MoviePy, IPython <br />
Tools/Technologies: Youtube API Client & Auth, Bing search API, Azure Cognitive Services, Docker </p>

<h2>Implementation</h2>
<li>The bot checks if the provided YouTube link is valid and then downloads the video using Pytube. </li> 
<li>It then utilizes MoviePy to cut the video into clips according to the timestamp in the video description. </li>
<li>A Chapter object is created for every single clip. It includes title, description, thumbnail, and start time of the clip.</li>
<li>A clip related image is downloaded using Bing Search API. Using Pillow library it creates a green square and adds the image to the clip thumbnail. </li>
<li>Itt uploads the clips, thumbnails, and descriptions through YouTube Data API.</li>
<li>Finally, the bot is Dockerized and can run on any device</li>

<h2>Time & Effort</h2>
The project took ~21 hours in total, within a week.
