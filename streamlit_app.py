import streamlit as st
from pytube import YouTube

def get_video_streams(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        return streams
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []

def download_video(stream):
    try:
        stream.download()
        return f"Video '{stream.title}' has been successfully downloaded."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    st.title("YouTube Video Downloader")
    st.write("Enter the YouTube video URL below and click on the 'Fetch' button to see available qualities.")

    url = st.text_input("YouTube URL")

    if st.button("Fetch"):
        if url:
            streams = get_video_streams(url)
            if streams:
                quality_options = [f"{stream.resolution} ({stream.filesize // (1024 * 1024)} MB)" for stream in streams]
                selected_quality = st.selectbox("Select Quality", quality_options)
                if st.button("Download"):
                    selected_stream = streams[quality_options.index(selected_quality)]
                    message = download_video(selected_stream)
                    st.write(message)
            else:
                st.write("No video streams available for this URL.")
        else:
            st.write("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
