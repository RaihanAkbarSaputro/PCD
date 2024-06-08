import streamlit as st
from pytube import YouTube
import os
import re

# Fungsi untuk mendapatkan informasi tentang video dari URL
@st.cache(allow_output_mutation=True)
def get_info(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, type='video')
        details = {
            "image": yt.thumbnail_url,
            "streams": streams,
            "title": yt.title,
            "length": yt.length,
            "itag": [stream.itag for stream in streams],
            "resolutions": [stream.resolution for stream in streams],
            "fps": [stream.fps for stream in streams],
            "format": [stream.subtype for stream in streams]
        }
        return details
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Setup folder untuk menyimpan video
directory = 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="YouTube Downloader", page_icon="🚀", layout="wide")

# Fungsi utama
def main():
    st.title("YouTube Downloader 🚀")
    url = st.text_input("Paste URL here 👇", key="url_input")
    
    if st.button("Tekan"):
        if url:
            v_info = get_info(url)
            if v_info:
                col1, col2 = st.columns([1, 1.5])
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
                        file_name = st.text_input('__Save as 🎯__', placeholder=v_info['title'] + ".mp4")
                button = st.button("Download ⚡️")
                if button:
                    with st.spinner('Downloading...'):
                        try:
                            selected_stream = v_info["streams"].get_by_itag(v_info['itag'][id])
                            output_path = os.path.join(directory, file_name)
                            selected_stream.download(output_path=output_path, filename=file_name)
                            st.success('Download Complete', icon="✅")
                            st.markdown(f"[Download Video]({output_path})")  # Tampilkan tautan unduhan
                            st.balloons()
                        except:
                            st.error('Error: Save with a different name!', icon="🚨")
            else:
                st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
