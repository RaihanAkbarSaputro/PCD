import streamlit as st
from pytube import YouTube
import os
import re
import tempfile

st.set_page_config(
    page_title="YTD ", page_icon="🚀", layout="wide",)
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1516557070061-c3d1653fa646?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

def download_video(video_url, itag, output_path, filename):
    yt = YouTube(video_url)
    stream = yt.streams.get_by_itag(itag)
    with st.spinner("Downloading... Please wait."):
        stream.download(output_path=output_path, filename=filename)
    st.success(f"Download Completed: {filename}")

@st.cache(allow_output_mutation=True)
def get_info(url):
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, type='video')
    details = {}
    details["image"] = yt.thumbnail_url
    details["streams"] = streams
    details["title"] = yt.title
    details["length"] = yt.length
    itag, resolutions, vformat, frate = ([] for i in range(4))
    for i in streams:
        res = re.search(r'(\d+)p', str(i))
        typ = re.search(r'video/(\w+)', str(i))
        fps = re.search(r'(\d+)fps', str(i))
        tag = re.search(r'(\d+)', str(i))
        itag.append(str(i)[tag.start():tag.end()])
        resolutions.append(str(i)[res.start():res.end()])
        vformat.append(str(i)[typ.start():typ.end()])
        frate.append(str(i)[fps.start():fps.end()])
    details["resolutions"] = resolutions
    details["itag"] = itag
    details["fps"] = frate
    details["format"] = vformat
    return details

st.title("YouTube Downloader 🚀")
url = st.text_input("Paste URL here 👇", placeholder='https://www.youtube.com/')
if url:
    v_info = get_info(url)
    col1, col2 = st.columns([1, 1.5], gap="small")
    with st.container():
        with col1:
            st.image(v_info["image"])
        with col2:
            st.subheader("Video Details ⚙️")
            res_inp = st.selectbox('__Select Resolution__', v_info["resolutions"])
            id = v_info["resolutions"].index(res_inp)
            st.write(f"__Title:__ {v_info['title']}")
            st.write(f"__Length:__ {v_info['length']} sec")
            st.write(f"__Resolution:__ {v_info['resolutions'][id]}")
            st.write(f"__Frame Rate:__ {v_info['fps'][id]}")
            st.write(f"__Format:__ {v_info['format'][id]}")
            file_name = st.text_input('__Save as 🎯__', placeholder=v_info['title'])
            if file_name:
                file_name = re.sub(r'[\\/*?:"<>|]', '', file_name) + ".mp4"
            else:
                file_name = re.sub(r'[\\/*?:"<>|]', '', v_info['title']) + ".mp4"

    if st.button("Download ⚡️"):
        with tempfile.TemporaryDirectory() as temp_dir:
            download_video(url, v_info['itag'][id], temp_dir, file_name)
            with open(os.path.join(temp_dir, file_name), "rb") as f:
                data = f.read()
            st.download_button(label="Click to download", data=data, file_name=file_name)
